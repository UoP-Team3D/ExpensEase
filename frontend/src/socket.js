import { io } from 'socket.io-client';
const socket = io();

socket.on('connect', () => {
    console.log('WebSocket connected');
  });
  
  socket.on('disconnect', () => {
    console.log('WebSocket disconnected');
  });

socket.on('low_budget_notification', function(data) {
  const { category_name, current_amount } = data;
    alert(`Your budget for the category '${category_name}' is running low. Current amount: £${current_amount.toFixed(2)}`);
  });

export default socket;