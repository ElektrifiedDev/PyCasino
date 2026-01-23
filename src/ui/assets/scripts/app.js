window.addEventListener('pywebviewready', function() {
    // Set up persistent buttons
    document.getElementById('create-save-btn').onclick = async () => {
        await pywebview.api.create_save_file();
        renderSaves();
    };

    document.getElementById('close-game-btn').onclick = () => {
        showScreen('hub-screen');
        document.getElementById('game-content').innerHTML = ''; // Clear game data
    };

    document.getElementById('logout-btn').onclick = () => showScreen('menu-screen');

    initializeApp();
});

// Primary screen switcher
function showScreen(screenId) {
    document.querySelectorAll('.app-screen').forEach(s => s.classList.remove('active'));
    const target = document.getElementById(screenId);
    if (target) target.classList.add('active');
}

async function renderSaves() {
    const saveList = document.getElementById('save-list');
    const saves = await pywebview.api.fetch_saves();
    saveList.innerHTML = '';

    saves.forEach(saveFile => {
        const btn = document.createElement('button');
        btn.className = 'save-item';
        btn.innerText = `Load: ${saveFile}`;
        btn.onclick = () => selectSave(saveFile);
        saveList.appendChild(btn);
    });
}

async function selectSave(filename) {
    const result = await pywebview.api.verify_save(filename);
    if (result.success) {
        document.getElementById('balance-val').innerText = result.data.balance;
        showScreen('hub-screen');
    } else {
        alert("Tampered save: " + result.message);
    }
}

// Logic to inject game fragments instead of using iframes
async function loadGame(gameName) {
    const container = document.getElementById('game-content');
    try {
        const response = await fetch(`./games/${gameName}.html`);
        const html = await response.text();
        container.innerHTML = html;

        // Manually execute scripts inside the fragment
        const scripts = container.querySelectorAll("script");
        scripts.forEach(oldScript => {
            const newScript = document.createElement("script");
            newScript.text = oldScript.text;
            document.body.appendChild(newScript).parentNode.removeChild(newScript);
        });

        showScreen('game-viewport');
    } catch (e) {
        console.error("Game load failed", e);
    }
}

async function initializeApp() {
    await renderSaves();
    const settings = await pywebview.api.load_settings();
    if (settings.theme === 'dark') {
        document.body.classList.add('dark-theme');
    }
    showScreen('menu-screen');
}