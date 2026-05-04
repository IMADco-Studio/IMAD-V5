const logOutput = document.getElementById('logOutput');
const validateBtn = document.getElementById('validateBtn');
const startBtn = document.getElementById('startBtn');

function addLog(message, type = 'info') {
    const p = document.createElement('p');
    p.className = `${type}-msg`;
    const time = new Date().toLocaleTimeString();
    p.textContent = `[${time}] > ${message}`;
    logOutput.appendChild(p);
    logOutput.scrollTop = logOutput.scrollHeight;
}

validateBtn.addEventListener('click', async () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!email || !password) return addLog("Please enter email and password.", "error");

    addLog("Attempting Stealth Login...", "info");
    
    try {
        const response = await fetch('http://localhost:8000/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, post_id: "0", comments: [] })
        });
        
        const data = await response.json();
        if (response.ok) {
            addLog("SUCCESS: Stealth Login Verified.", "success");
        } else {
            addLog(`ERROR: ${data.detail || "Login failed."}`, "error");
        }
    } catch (err) {
        addLog("Could not connect to the backend server.", "error");
    }
});

startBtn.addEventListener('click', async () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const postId = document.getElementById('postId').value;
    const commentsText = document.getElementById('comments').value;
    const minDelay = parseInt(document.getElementById('minDelay').value);
    const maxDelay = parseInt(document.getElementById('maxDelay').value);

    if (!email || !password || !postId || !commentsText) {
        return addLog("Missing required fields.", "error");
    }

    const comments = commentsText.split('\n').filter(c => c.trim() !== '');

    addLog(`Initializing Stealth Bot for post ${postId}...`, "info");

    try {
        const response = await fetch('http://localhost:8000/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                email,
                password,
                post_id: postId, 
                comments, 
                min_delay: minDelay, 
                max_delay: maxDelay 
            })
        });

        const data = await response.json();
        if (response.ok) {
            addLog(`SUCCESS: ${data.message}`, "success");
            addLog("Automation is now running in Stealth Mode.", "success");
            startBtn.disabled = true;
            startBtn.textContent = "BOT RUNNING";
        } else {
            addLog(`FAILED: ${data.detail || "Unknown error"}`, "error");
        }
    } catch (err) {
        addLog("Connection failed. Ensure backend is active.", "error");
    }
});
