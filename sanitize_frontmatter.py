import os
import yaml

def sanitize_file(filepath):
    try:
        # utf-8-sig remueve la firma BOM invisible de Windows/Obsidian
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        # Quartz's gray-matter ignora espacios y saltos de linea vacios al inicio
        stripped_content = content.lstrip()
        if not stripped_content.startswith('---'):
            return

        lines = content.splitlines()
        
        # Encontrar exactamente la linea del primer '---'
        start_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '---':
                start_idx = i
                break
                
        if start_idx == -1:
            return

        end_idx = -1
        for i in range(start_idx + 1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break

        modified = False

        if end_idx == -1:
            # Sin cerrar
            lines.pop(start_idx)
            content = '\n'.join(lines)
            modified = True
        else:
            frontmatter_block = '\n'.join(lines[start_idx + 1 : end_idx])
            try:
                parsed = yaml.safe_load(frontmatter_block)
                # Parse puede devolver None si esta vacio. Si no es dict ni None, es invalido.
                if parsed is not None and not isinstance(parsed, dict):
                    raise ValueError("Not a dictionary")
            except Exception:
                # Falla el parseo estricto
                lines.pop(start_idx)
                content = '\n'.join(lines)
                modified = True

        if modified:
            # Escribir con utf-8 normal sin BOM
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[Sanitizado correctamente] {filepath}")

    except Exception as e:
        print(f"Error procesando {filepath}: {e}")

def main():
    content_dir = os.path.join(os.getcwd(), 'content')
    if not os.path.exists(content_dir):
        print("El directorio 'content' no existe.")
        return
        
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                sanitize_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
