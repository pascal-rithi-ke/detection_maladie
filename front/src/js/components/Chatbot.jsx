import React, { useState, useEffect } from 'react';
import '../../css/Chatbot.css';

const Chatbot = () => {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const [typingMessage, setTypingMessage] = useState(''); // Message en cours d'écriture

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSendMessage = async () => {
        if (input.trim() !== '') {
            const userMessage = { text: input, user: 'user' };
            setMessages([...messages, userMessage]);
            setInput('');
            setIsTyping(true);

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
                    const fullMessage = data.response;
                    let index = 0;
                    setTypingMessage(''); // Reset message en cours d'écriture

                    // Effet "tape writing"
                    const typingInterval = setInterval(() => {
                        setTypingMessage((prev) => prev + fullMessage[index]);
                        index++;

                        if (index === fullMessage.length) {
                            clearInterval(typingInterval);
                            setIsTyping(false);
                            setMessages((prevMessages) => [
                                ...prevMessages,
                                { text: fullMessage, user: 'bot' },
                            ]);
                            setTypingMessage(''); // Clear typing message
                        }
                    }, 35); // Intervalle de 35ms pour ajouter chaque lettre
                } else {
                    console.error('Server error:', response.statusText);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const clearMessage = () => {
        setMessages([]);
    };

    const renderMessageText = (text) => {
        return text.split('\n').map((line, index) => (
            <React.Fragment key={index}>
                {line}
                <br />
            </React.Fragment>
        ));
    };

    return (
        <div className="chatbot">
            <div className="chatbot-messages">
                {messages.map((message, index) => (
                    <div key={index} className={`chatbot-message ${message.user}`}>
                        {renderMessageText(message.text)}
                    </div>
                ))}
                {isTyping && (
                    <div className="chatbot-message bot typing">
                        {typingMessage === '' ? "Bot is typing..." : renderMessageText(typingMessage)}
                    </div>
                )}
            </div>
            <div className="chatbot-input">
                <textarea
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Type a message..."
                    rows="1"
                />
                <div className='chatbot-buttons'>
                    <button onClick={handleSendMessage}>
                        <img className='arrow' src="../src/img/arrow.svg"/>
                    </button>
                    <button className='new-chat' onClick={clearMessage}>
                        <img className='chat' src="../src/img/write.png"/>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;