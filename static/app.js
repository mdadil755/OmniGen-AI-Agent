let activeImageB64 = null;

async function submitMessage() {
    const inputNode = document.getElementById("userInput");
    const chatContainer = document.getElementById("chatContainer");
    const canvasBox = document.getElementById("canvasBox");
    const statusNode = document.getElementById("statusIndicator");
    const intentNode = document.getElementById("intentIndicator");
    const promptLogNode = document.getElementById("expandedPromptText");
    const downloadNode = document.getElementById("downloadBtn");
    
    const promptValue = inputNode.value.trim();
    if (!promptValue) return;

    chatContainer.innerHTML += `<div class="bg-gray-800 p-2 rounded text-sm text-white border-l-4 border-blue-500"><b>User:</b> ${promptValue}</div>`;
    canvasBox.innerHTML = `<div class="text-blue-500 animate-pulse text-sm font-mono tracking-wider text-center">🔄 Intercepting Tokens...<br>Running Neural Inference Matrix</div>`;
    
    statusNode.innerText = "Engine: Processing...";
    statusNode.classList.add("text-blue-400");
    inputNode.value = "";
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Network connection controller setup kiya drop bachane ke liye
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minutes timeout extension

    try {
        const response = await fetch('/process_chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            signal: controller.signal,
            body: JSON.stringify({
                message: promptValue,
                last_image: activeImageB64
            })
        });
        
        clearTimeout(timeoutId);
        const data = await response.json();

        if (data.error) {
            chatContainer.innerHTML += `<div class="bg-red-950 text-red-400 p-2 rounded text-xs border border-red-900"><b>Engine Halted:</b> ${data.error}</div>`;
            canvasBox.innerHTML = `<div class="text-gray-600 text-sm">Pipeline Execution Failed.</div>`;
            statusNode.innerText = "Engine: Halted";
            return;
        }

        activeImageB64 = data.active_image;
        canvasBox.innerHTML = `<img src="${data.active_image}" class="max-h-full max-w-full object-contain rounded shadow-lg">`;
        promptLogNode.innerText = data.expanded_prompt;
        intentNode.innerText = `Intent: ${data.intent_used}`;
        statusNode.innerText = "Engine: Idle";
        statusNode.classList.remove("text-blue-400");
        
        downloadNode.href = data.active_image;
        downloadNode.classList.remove("pointer-events-none", "opacity-50");
        
        chatContainer.innerHTML += `<div class="bg-gray-900 p-2 rounded text-xs text-green-400 border border-gray-800"><b>Agent:</b> Frame rendered successfully.</div>`;
        chatContainer.scrollTop = chatContainer.scrollHeight;

    } catch (err) {
        clearTimeout(timeoutId);
        canvasBox.innerHTML = `<div class="text-red-500 text-sm text-center">Network Matrix Disconnected.<br><span class="text-xxs text-gray-500">Reason: Connection dropped or timeout. Please retry.</span></div>`;
        statusNode.innerText = "Engine: Timeout/Drop";
    }
          }
