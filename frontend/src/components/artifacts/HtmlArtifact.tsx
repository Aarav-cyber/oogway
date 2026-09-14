import React, { useMemo } from 'react';
import { sanitizeHtmlContent } from '../../lib/sanitize';

interface HtmlArtifactProps {
  content: string;
}

export const HtmlArtifact: React.FC<HtmlArtifactProps> = ({ content }) => {
  const sanitizedHtml = useMemo(() => {
    const cleanContent = sanitizeHtmlContent(content);
    return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body {
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
              padding: 1.5rem;
              margin: 0;
              background-color: #0f172a;
              color: #f8fafc;
              line-height: 1.6;
            }
            h1, h2, h3, h4 { color: #38bdf8; }
            a { color: #34d399; }
            code, pre { background-color: #1e293b; padding: 0.2rem 0.4rem; border-radius: 0.25rem; font-family: monospace; }
          </style>
        </head>
        <body>
          ${cleanContent}
        </body>
      </html>
    `;
  }, [content]);

  return (
    <div className="flex-1 w-full h-full bg-slate-950 flex flex-col overflow-hidden">
      <iframe
        title="Artifact HTML Preview"
        srcDoc={sanitizedHtml}
        sandbox="allow-same-origin allow-popups"
        className="w-full h-full border-0 bg-slate-950"
      />
    </div>
  );
};
