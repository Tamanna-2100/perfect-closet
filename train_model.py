"""
Model Training Script for Body Type Classification
Uses the existing dataset to train a ResNet50 model
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from torchvision.datasets import ImageFolder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BodyTypeDataset(Dataset):
    """Custom dataset for body type classification"""
    
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

class BodyTypeClassifierTrainer:
    def __init__(self, data_dir, model_save_path='models/body_type_classifier.pth'):
        self.data_dir = data_dir
        self.model_save_path = model_save_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.body_types = ['Apple', 'Hourglass', 'Inverted Triangle', 'Rectangle', 'Triangle']
        
        # Create models directory
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        
        logger.info(f"Using device: {self.device}")
        
    def get_transforms(self):
        """Define data augmentation and preprocessing transforms"""
        train_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        val_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        return train_transform, val_transform
    
    def load_data_from_existing_dataset(self):
        """Load data from the existing temp_dataset structure"""
        image_paths = []
        labels = []
        
        # Check if we have the Body Types Images folder
        body_types_dir = os.path.join(self.data_dir, 'Body Types Images')
        if os.path.exists(body_types_dir):
            for filename in os.listdir(body_types_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Extract body type from filename
                    body_type = filename.split('.')[0]
                    if body_type in self.body_types:
                        image_path = os.path.join(body_types_dir, filename)
                        image_paths.append(image_path)
                        labels.append(self.body_types.index(body_type))
        
        # Also check for segmentation images
        seg_dir = os.path.join(self.data_dir, 'Body Types Segmentation Images')
        if os.path.exists(seg_dir):
            for filename in os.listdir(seg_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Extract body type from filename (remove 'Seg' suffix)
                    body_type = filename.replace(' Seg', '').split('.')[0]
                    if body_type in self.body_types:
                        image_path = os.path.join(seg_dir, filename)
                        image_paths.append(image_path)
                        labels.append(self.body_types.index(body_type))
        
        logger.info(f"Found {len(image_paths)} images across {len(set(labels))} body types")
        return image_paths, labels
    
    def create_model(self):
        """Create ResNet50 model for body type classification"""
        model = models.resnet50(pretrained=True)
        
        # Freeze early layers
        for param in model.parameters():
            param.requires_grad = False
            
        # Unfreeze last few layers
        for param in model.layer4.parameters():
            param.requires_grad = True
            
        # Replace final classifier
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, len(self.body_types))
        )
        
        return model.to(self.device)
    
    def train_epoch(self, model, dataloader, criterion, optimizer, epoch):
        """Train for one epoch"""
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(dataloader, desc=f'Epoch {epoch+1} Training')
        for images, labels in pbar:
            images, labels = images.to(self.device), labels.to(self.device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            pbar.set_postfix({
                'Loss': f'{running_loss/len(dataloader):.4f}',
                'Acc': f'{100*correct/total:.2f}%'
            })
        
        return running_loss / len(dataloader), 100 * correct / total
    
    def validate(self, model, dataloader, criterion):
        """Validate the model"""
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        all_predicted = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in tqdm(dataloader, desc='Validation'):
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                running_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
                all_predicted.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        accuracy = 100 * correct / total
        avg_loss = running_loss / len(dataloader)
        
        return avg_loss, accuracy, all_predicted, all_labels
    
    def plot_training_history(self, train_losses, train_accs, val_losses, val_accs):
        """Plot training history"""
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(train_losses, label='Training Loss')
        plt.plot(val_losses, label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(train_accs, label='Training Accuracy')
        plt.plot(val_accs, label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy (%)')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.body_types,
                   yticklabels=self.body_types)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png')
        plt.show()
    
    def train(self, epochs=50, batch_size=16, learning_rate=0.001):
        """Main training function"""
        logger.info("Starting training process...")
        
        # Load data
        image_paths, labels = self.load_data_from_existing_dataset()
        
        if len(image_paths) == 0:
            logger.error("No images found! Please check your data directory.")
            return
        
        # Split data
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            image_paths, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Get transforms
        train_transform, val_transform = self.get_transforms()
        
        # Create datasets
        train_dataset = BodyTypeDataset(train_paths, train_labels, train_transform)
        val_dataset = BodyTypeDataset(val_paths, val_labels, val_transform)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
        
        # Create model
        model = self.create_model()
        
        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.5)
        
        # Training history
        train_losses, train_accs = [], []
        val_losses, val_accs = [], []
        best_val_acc = 0.0
        
        logger.info(f"Training on {len(train_dataset)} samples, validating on {len(val_dataset)} samples")
        
        for epoch in range(epochs):
            # Train
            train_loss, train_acc = self.train_epoch(model, train_loader, criterion, optimizer, epoch)
            train_losses.append(train_loss)
            train_accs.append(train_acc)
            
            # Validate
            val_loss, val_acc, val_pred, val_true = self.validate(model, val_loader, criterion)
            val_losses.append(val_loss)
            val_accs.append(val_acc)
            
            # Update learning rate
            scheduler.step()
            
            logger.info(f'Epoch {epoch+1}/{epochs}:')
            logger.info(f'  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
            logger.info(f'  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
            
            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), self.model_save_path)
                logger.info(f'  New best model saved with validation accuracy: {best_val_acc:.2f}%')
        
        # Plot results
        self.plot_training_history(train_losses, train_accs, val_losses, val_accs)
        
        # Final evaluation
        logger.info("Final evaluation:")
        logger.info(f"Best validation accuracy: {best_val_acc:.2f}%")
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(val_true, val_pred, target_names=self.body_types))
        
        # Confusion matrix
        self.plot_confusion_matrix(val_true, val_pred)
        
        logger.info(f"Model saved to: {self.model_save_path}")

def main():
    """Main function to run training"""
    # Set the path to your dataset
    data_dir = "temp_dataset"  # Update this path
    
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} not found!")
        return
    
    # Create trainer
    trainer = BodyTypeClassifierTrainer(data_dir)
    
    # Start training
    trainer.train(epochs=30, batch_size=8, learning_rate=0.001)

if __name__ == "__main__":
    main()