import React, { useState } from 'react';
import '../../css/Chatbot.css';

const Chatbot = () => {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSendMessage = async () => {
        if (input.trim() !== '') {
            const userMessage = { text: input, user: 'user' };
            setMessages([...messages, userMessage]);

            try {
                const response = await fetch('http://localhost:5000/chatbot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: input }),
                });

                if (response.ok) {
                    const data = await response.json();
                    const botMessage = { text: data.response, user: 'bot' };
                    setMessages((prevMessages) => [...prevMessages, botMessage]);
                } else {
                    console.error('Server error:', response.statusText);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }

            setInput('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="chatbot">
            <div className="chatbot-messages">
                {messages.map((message, index) => (
                    <div key={index} className={`chatbot-message ${message.user}`}>
                        {message.text}
                    </div>
                ))}
            </div>
            <div className="chatbot-input">
                <textarea
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Type a message..."
                    rows="1"
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
