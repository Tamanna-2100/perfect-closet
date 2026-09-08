"use client";

import React, { useState } from "react";
import { ProductSuggestion } from "@/types";
import { ExternalLink, Tag } from "lucide-react";

interface ProductCatalogProps {
  products: ProductSuggestion[];
}

const CATEGORIES = ["All", "Tops", "Dresses", "Outerwear", "Pants"];

export const ProductCatalog: React.FC<ProductCatalogProps> = ({ products }) => {
  const [selectedCategory, setSelectedCategory] = useState("All");

  const filteredProducts =
    selectedCategory === "All"
      ? products
      : products.filter(
          (p) => p.garment_type.toLowerCase() === selectedCategory.toLowerCase()
        );

  return (
    <div className="w-full space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-serif text-stone-100 font-normal">
            Retail Fashion Matches
          </h2>
          <p className="text-xs text-stone-400 mt-1">
            Current Google Shopping listings tailored to your chromatic coordinates.
          </p>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 sm:pb-0">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`text-xs px-3.5 py-1.5 rounded-full font-medium transition-all ${
                selectedCategory === cat
                  ? "bg-stone-200 text-stone-950 shadow"
                  : "bg-stone-900/60 text-stone-400 hover:text-stone-200 border border-stone-800"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filteredProducts.map((prod) => (
          <div
            key={prod.id}
            className="group rounded-2xl bg-stone-900/40 border border-stone-800 overflow-hidden hover:border-stone-700 transition-all duration-300 flex flex-col shadow-lg"
          >
            <div className="relative aspect-[3/4] overflow-hidden bg-stone-950">
              <img
                src={prod.image_url}
                alt={prod.title}
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <div className="absolute top-3 left-3 bg-stone-950/80 backdrop-blur-sm border border-stone-800 text-[10px] text-stone-300 px-2 py-0.5 rounded font-mono">
                {prod.merchant}
              </div>
              <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between">
                <div className="flex items-center gap-1.5 bg-stone-950/90 backdrop-blur-sm px-2 py-1 rounded-md border border-stone-800 text-[10px] text-stone-200 font-mono">
                  <span
                    className="w-2.5 h-2.5 rounded-full border border-stone-700 inline-block"
                    style={{ backgroundColor: prod.color_hex }}
                  />
                  <span>{prod.color_name}</span>
                </div>
                <div className="bg-emerald-950/90 text-emerald-300 text-[10px] font-mono px-2 py-1 rounded-md border border-emerald-800/60">
                  {prod.match_score.toFixed(0)}% Match
                </div>
              </div>
            </div>

            <div className="p-4 flex-1 flex flex-col justify-between">
              <div>
                <h4 className="text-xs font-medium text-stone-200 font-sans line-clamp-2 leading-snug">
                  {prod.title}
                </h4>
                <div className="mt-2 text-[11px] text-stone-400 font-mono flex items-center gap-1">
                  <Tag className="w-3 h-3 text-stone-500" />
                  <span>{prod.cut}</span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-stone-800/60 flex items-center justify-between">
                <span className="text-sm font-semibold text-stone-100 font-mono">
                  {prod.price}
                </span>
                <a
                  href={prod.product_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-amber-300 hover:text-amber-200 font-medium flex items-center gap-1 transition-colors"
                >
                  Buy Now <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
