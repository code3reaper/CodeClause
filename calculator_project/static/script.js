document.addEventListener('DOMContentLoaded', () => {
    const display = document.getElementById('display');
    const historyDisplay = document.getElementById('history');
    const buttons = document.querySelectorAll('.btn');

    // Function to send button value to Python backend
    const sendButtonPress = async (value) => {
        try {
            const response = await fetch('/button_press', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ value: value })
            });
            const data = await response.json();
            // Update the display with the values sent by Python
            display.textContent = data.display;
            historyDisplay.textContent = data.history;
        } catch (error) {
            console.error('Error sending button press:', error);
            display.textContent = 'Comm Error'; // Indicate a communication error
            historyDisplay.textContent = 'Check server';
        }
    };

    // Attach click listeners to all buttons
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.dataset.value;
            sendButtonPress(value);
        });
    });

    // Initial state setup: Request the initial state from Python when the page loads
    // This ensures '0' is displayed correctly on initial load.
    sendButtonPress('');
});