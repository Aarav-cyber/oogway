import DOMPurify from 'dompurify';

export function sanitizeHtmlContent(htmlContent: string): string {
  if (!htmlContent) return '';

  return DOMPurify.sanitize(htmlContent, {
    ADD_TAGS: ['style'],
    ADD_ATTR: ['target', 'style', 'class', 'id'],
    FORBID_TAGS: ['script', 'iframe', 'object', 'embed', 'form'],
    FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover'],
  });
}
