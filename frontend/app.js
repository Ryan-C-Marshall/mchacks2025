function changeTitle(ev) {
  document.getElementById("title").textContent = "hello";
}

function testFun() {
  changeTitle();
}

console.log('hello');

document.getElementById('prompt-box-id').addEventListener("submit", async (event) => {
  
  
    event.preventDefault(); 
    
    const prompt = document.getElementById('prompt-id').value;

    // Send the prompt to your backend
    const response = await fetch('http://127.0.0.1:5000/process-prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt }),
    });

    const result = await response.json();
    console.log('Result from backend:', result);
  
});