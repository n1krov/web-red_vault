import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/footer.scss"
//imports opcionales removidos

interface Options {
  links: Record<string, string>
}

export default ((opts?: Options) => {
  const Footer: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
    const year = new Date().getFullYear()
    const links = opts?.links ?? []
    return (
      <footer class={`${displayClass ?? ""}`}>
        <p>
          Hecho por <b>n1krov</b> y <b>universoparalelo</b> © {year}
        </p>
        <ul>
          {Object.entries(links).map(([text, link]) => (
            <li>
              <a href={link}>{text}</a>
            </li>
          ))}
        </ul>
      </footer>
    )
  }

  Footer.css = style
  Footer.afterDOMLoaded = `
    const el = document.getElementById("typewriter");
    if (el) {
      const commands = [
        "nmap -sC -sV 10.10.10.1",
        "cat /etc/shadow",
        "cat /etc/passwd",
        "cat ~/.config/kotetsu",
        "nvim ~/.config/liskov",
        "ssh root@red_vault",
        "sudo rm -rf /*",
        "whoami"
      ];
      let cmdIndex = 0;
      let charIndex = 0;
      let isDeleting = false;
      let timer;
      el.textContent = "";
      function type() {
        if (!document.getElementById("typewriter")) return; 
        const currentCmd = commands[cmdIndex];
        if (isDeleting) {
          el.textContent = currentCmd.substring(0, charIndex - 1);
          charIndex--;
        } else {
          el.textContent = currentCmd.substring(0, charIndex + 1);
          charIndex++;
        }
        let typeSpeed = isDeleting ? 30 : Math.random() * 50 + 50;
        if (!isDeleting && charIndex === currentCmd.length) {
          typeSpeed = 3000;
          isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
          isDeleting = false;
          cmdIndex = (cmdIndex + 1) % commands.length;
          typeSpeed = 500;
        }
        timer = setTimeout(type, typeSpeed);
      }
      clearTimeout(timer);
      setTimeout(type, 1000);
    }
  `
  return Footer
}) satisfies QuartzComponentConstructor
