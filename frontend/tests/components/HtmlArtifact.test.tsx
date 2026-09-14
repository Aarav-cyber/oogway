import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { HtmlArtifact } from '../../src/components/artifacts/HtmlArtifact';

describe('HtmlArtifact Component', () => {
  it('renders iframe with sandbox security controls', () => {
    const htmlContent = '<div><h1>Dashboard Summary</h1><script>alert("xss")</script></div>';
    const { container } = render(<HtmlArtifact content={htmlContent} />);

    const iframe = container.querySelector('iframe');
    expect(iframe).not.toBeNull();
    expect(iframe?.getAttribute('sandbox')).toContain('allow-same-origin');
    expect(iframe?.getAttribute('srcdoc')).toContain('<h1>Dashboard Summary</h1>');
    expect(iframe?.getAttribute('srcdoc')).not.toContain('<script>');
  });
});
