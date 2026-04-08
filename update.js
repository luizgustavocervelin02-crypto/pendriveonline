const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf-8');

// Helper to remove between substrings
function removeBetween(startStr, endStr) {
    let startIdx = html.indexOf(startStr);
    if (startIdx !== -1) {
        let endIdx = html.indexOf(endStr, startIdx);
        if (endIdx !== -1) {
            html = html.substring(0, startIdx) + html.substring(endIdx + endStr.length);
            console.log('Removed matching string starting with: ' + startStr.substring(0, 30) + '...');
        } else {
            console.log('WARNING: endStr not found for: ' + startStr.substring(0, 30));
        }
    } else {
        console.log('WARNING: startStr not found: ' + startStr.substring(0, 30));
    }
}

// 1. Hero background div -> img
const heroStart = '<div class="fixed inset-0 bg-cover bg-center bg-no-repeat opacity-20 pointer-events-none" style="background-image:url(&#x27;https://i.ibb.co/9mrMkF3v/';
const heroEnd = '&#x27;)"></div>';
const newHero = '<img src="https://i.ibb.co/tMR4mJXt/1w1.jpg" width="1080" height="1920" loading="eager" fetchpriority="high" decoding="sync" class="fixed inset-0 w-full h-full object-cover opacity-20 pointer-events-none" style="z-index: 0;" alt="Hero Background">';

let hStartIdx = html.indexOf(heroStart);
if (hStartIdx !== -1) {
    let hEndIdx = html.indexOf(heroEnd, hStartIdx);
    if (hEndIdx !== -1) {
        html = html.substring(0, hStartIdx) + newHero + html.substring(hEndIdx + heroEnd.length);
        console.log('Hero image replaced.');
    }
} else {
    console.log('WARNING: heroStart not found.');
}

// 1b. Update preload image link
let plStart = '<link rel="preload" as="image" href="https://i.ibb.co/9mrMkF3v';
let plEnd = 'fetchpriority="high">';
if (html.indexOf(plStart) !== -1) {
    removeBetween(plStart, plEnd);
    html = html.replace('href="assets/logo.png" fetchpriority="high">', 'href="assets/logo.png" fetchpriority="high"><link rel="preload" as="image" href="https://i.ibb.co/tMR4mJXt/1w1.jpg" fetchpriority="high">');
    console.log('Preload link updated.');
} else {
    console.log('WARNING: Preload link not found.');
}

// 2. Head section top navbar
removeBetween('<header class="bg-black/80 backdrop-blur-sm', '</header>');

// 3. Section metrics
removeBetween('<div class="grid grid-cols-3 gap-4 mb-8 max-w-md mx-auto">', 'Avaliacao</p></div></div>');

// 4. Badge ATUALIZADO EM MARÇO 2026
removeBetween('<span data-slot="badge"', 'ATUALIZADO EM MARCO 2026</span>');

// 5. Botão VEJA O VIDE
removeBetween('<span data-slot="badge"', 'VEJA O VIDEO</span>');

// 6. Contador regressivo
removeBetween('<div class="bg-black/50 rounded-xl p-4 mt-6 border border-white/10">', 'SEG</p></div></div></div></div>');

// 7. Bloco de oferta com preço 70% OFF 
// Wait, looking at the previous file view, there is a section tag. Let me verify the exact string.
removeBetween('<section class="py-12 px-4 bg-gradient-to-b from-neutral-900/90 to-neutral-950/90 relative z-10">', '</section>');

fs.writeFileSync('index.html', html, 'utf-8');
console.log('Update Complete.');
