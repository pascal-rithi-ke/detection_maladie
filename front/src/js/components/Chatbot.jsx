import React, { useState, useEffect, useRef } from 'react';
import '../../css/Chatbot.css';

const Chatbot = () => {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const [typingMessage, setTypingMessage] = useState(''); // Message en cours d'écriture
    const typingIntervalRef = useRef(null); // Ref pour l'intervalle

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSendMessage = async () => {
        if (input.trim() !== '') {
            const userMessage = { text: input, user: 'user' };
            setMessages([...messages, userMessage]);
            setInput(''); // Efface le champ d'input seulement après l'envoi
            setIsTyping(true); // Désactive l'envoi pendant que le bot tape

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
                    typingIntervalRef.current = setInterval(() => {
                        setTypingMessage((prev) => prev + fullMessage[index]);
                        index++;

                        if (index === fullMessage.length) {
                            clearInterval(typingIntervalRef.current);
                            setIsTyping(false); // Réactive l'envoi après que le bot a fini
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
        if (e.key === 'Enter' && !e.shiftKey && !isTyping) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const clearMessage = () => {
        setMessages([]); // Clear all messages
        setIsTyping(false); // Ensure the typing status is reset
        setTypingMessage(''); // Clear the message that was in typing state
        if (typingIntervalRef.current) {
            clearInterval(typingIntervalRef.current); // Clear the typing interval
            typingIntervalRef.current = null; // Reset the ref to null
        }
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
                    disabled={isTyping && input.trim() === ''} // Désactive si le bot tape et l'input est vide
                />
                <div className='chatbot-buttons'>
                    <button className='send' onClick={handleSendMessage} disabled={isTyping || input.trim() === ''}>
                        Send
                    </button>
                    <button className='send' onClick={clearMessage}>
                        New chat
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
