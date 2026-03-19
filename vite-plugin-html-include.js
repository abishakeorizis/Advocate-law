import fs from 'fs';
import path from 'path';

/**
 * Vite plugin to include HTML partials.
 * Replaces <!-- include: filename.html --> directives with file contents.
 */
export default function htmlIncludePlugin() {
    return {
        name: 'html-include',
        enforce: 'pre',
        transformIndexHtml: {
            order: 'pre',
            handler(html, ctx) {
                const rootDir = ctx.server
                    ? ctx.server.config.root
                    : process.cwd();

                return html.replace(
                    /<!--\s*include:\s*(.+?)\s*-->/g,
                    (match, filePath) => {
                        const fullPath = path.resolve(rootDir, filePath.trim());
                        try {
                            return fs.readFileSync(fullPath, 'utf-8');
                        } catch (e) {
                            console.error(`[html-include] File not found: ${fullPath}`);
                            return `<!-- ERROR: Could not include ${filePath} -->`;
                        }
                    }
                );
            }
        },
        handleHotUpdate({ file, server }) {
            // Reload page when any HTML partial changes
            if (file.endsWith('.html')) {
                server.ws.send({ type: 'full-reload' });
            }
        }
    };
}
