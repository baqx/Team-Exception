"use client";

import React, { useMemo } from "react";
import katex from "katex";

interface MathTexProps {
  math: string;
  displayMode?: boolean;
  className?: string;
}

export function MathTex({ math, displayMode = false, className = "" }: MathTexProps) {
  const html = useMemo(() => {
    try {
      return katex.renderToString(math, {
        displayMode,
        throwOnError: false,
      });
    } catch {
      return math;
    }
  }, [math, displayMode]);

  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

/**
 * Parses a string containing inline math delimited by $...$ or $$...$$
 * and renders formatted KaTeX equations interspersed with plain text.
 */
export function FormattedChalkContent({ text, className = "" }: { text: string; className?: string }) {
  const parts = useMemo(() => {
    // Regex splits by $$...$$ or $...$
    const regex = /(\$\$[\s\S]+?\$\$|\$.+?\$)/g;
    const tokens = text.split(regex);

    return tokens.map((token, i) => {
      if (token.startsWith("$$") && token.endsWith("$$")) {
        const math = token.slice(2, -2).trim();
        return <MathTex key={i} math={math} displayMode={true} className="inline-block my-1" />;
      } else if (token.startsWith("$") && token.endsWith("$")) {
        const math = token.slice(1, -1).trim();
        return <MathTex key={i} math={math} displayMode={false} className="inline-block mx-0.5" />;
      }
      return <span key={i}>{token}</span>;
    });
  }, [text]);

  return <span className={className}>{parts}</span>;
}
