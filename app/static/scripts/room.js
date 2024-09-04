var socket = io()

socket.on('connect', () => {
  console.log('Connected to server')
  socket.emit('join_room', { room_name: roomName, username: username })
})


socket.on('message', (message) => {
  $('.list-unstyled').append(`<li class="list-group-item">
<strong>${message['username']}</strong>: <div class="message">${message['message']}</div> <div class="message-timestamp">(${message['timestamp']})</div>
</li>
`)
  $('.scrollable-card').scrollTop($('.scrollable-card')[0].scrollHeight)
})


let form = document.querySelector('form')
form.addEventListener('submit', (e) => {
  e.preventDefault()
  let message = document.querySelector('input')
  socket.emit('send_message', { message: message.value, username: username, room_name: roomName })
  message.value = ''
})


let leaveButton = document.querySelector('#leaveRoom')
leaveButton.addEventListener('click', () => {
  socket.emit('leave_room', { room_name: roomName, username: username })
  window.location.href = '/'
})
