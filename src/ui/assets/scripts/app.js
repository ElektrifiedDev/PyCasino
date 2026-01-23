// Function to run when the window is ready
window.addEventListener('pywebviewready', function() {
    console.log('PyWebView is ready');
    initializeApp();
});

async function initializeApp() {
    // 1. Load Settings (Volume, etc.)
    const settings = await pywebview.api.load_settings();
    console.log("Settings loaded:", settings);
    
    // 2. Fetch and Display Saves
    renderSaves();
}

async function renderSaves() {
    const saveList = document.getElementById('save-list');
    const saves = await pywebview.api.fetch_saves(); // Your Python function
    
    saveList.innerHTML = ''; // Clear "Loading..." text

    if (saves.length === 0) {
        saveList.innerHTML = '<p>No saves found.</p>';
        return;
    }

    saves.forEach(saveFile => {
        const btn = document.createElement('button');
        btn.className = 'save-item';
        btn.innerText = `Load: ${saveFile}`;
        btn.onclick = () => selectSave(saveFile);
        saveList.appendChild(btn);
    });
}

async function selectSave(filename) {
    // We send the filename back to Python to verify the Hash/DTN
    // You'll need a verify_save function in your main.py
    const result = await pywebview.api.verify_save(filename);

    if (result.success) {
        // Update UI with balance from the verified save
        document.getElementById('balance-val').innerText = result.data.balance;
        
        // Transition Screens
        document.getElementById('menu-screen').style.display = 'none';
        document.getElementById('hub-screen').style.display = 'block';
    } else {
        alert("Error: Save file is corrupted or tampered with!");
        console.error(result.message);
    }
}

// Function to load sub-games (dice.html, coinflip.html)
function loadGame(gameName) {
    const hub = document.getElementById('hub-screen');
    const viewport = document.getElementById('game-viewport');
    const frame = document.getElementById('game-frame');

    // Path relative to index.html based on your structure
    frame.src = `./games/${gameName}.html`;
    
    hub.style.display = 'none';
    viewport.style.display = 'block';
}

// Back to Lobby logic
document.getElementById('back-to-hub').onclick = () => {
    document.getElementById('game-viewport').style.display = 'none';
    document.getElementById('hub-screen').style.display = 'block';
    document.getElementById('game-frame').src = ''; // Stop the game process
};

// Create New Save logic
document.getElementById('create-save-btn').onclick = async () => {
    await pywebview.api.create_save_file();
    renderSaves(); // Refresh the list
};