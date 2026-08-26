const chat = document.getElementById('chat');
const chatContainer = document.getElementById('chatContainer');
const form = document.getElementById('chatForm');
const input = document.getElementById('pregunta');
const sendBtn = document.getElementById('sendBtn');
const closeBtn = document.getElementById('closeBtn');

function horaActual() {
  const ahora = new Date();
  return ahora.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
}

function agregarMensaje(texto, tipo) {
  const msg = document.createElement('div');
  msg.className = `msg ${tipo}`;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = texto;
  msg.appendChild(bubble);

  const hora = document.createElement('div');
  hora.className = 'timestamp';
  hora.textContent = horaActual();
  msg.appendChild(hora);

  chat.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return msg;
}

function mostrarEscribiendo() {
  const msg = document.createElement('div');
  msg.className = 'msg bot';
  msg.id = 'typingIndicator';
  msg.innerHTML = '<div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>';
  chat.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function quitarEscribiendo() {
  const el = document.getElementById('typingIndicator');
  if (el) el.remove();
}

async function enviarPregunta(pregunta) {
  agregarMensaje(pregunta, 'user');
  mostrarEscribiendo();
  sendBtn.disabled = true;

  try {
    const res = await fetch('/api/preguntar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta }),
    });
    console.log('Status:', res.status);
console.log('OK:', res.ok);
console.log('Content-Type:', res.headers.get('content-type'));

const texto = await res.text();
console.log('Respuesta del servidor:', texto);

quitarEscribiendo();

if (!res.ok) {
  agregarMensaje(`Error del servidor (${res.status}): ${texto}`, 'bot');
} else {
  const data = JSON.parse(texto);
  agregarMensaje(data.respuesta, 'bot');
}
  } catch (err) {
    quitarEscribiendo();
    agregarMensaje('No se pudo conectar con el servidor. Intentá de nuevo.', 'bot');
  } finally {
    sendBtn.disabled = false;
  }
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const pregunta = input.value.trim();
  if (!pregunta) return;
  input.value = '';
  enviarPregunta(pregunta);
});

agregarMensaje('¡Hola! Soy el asistente virtual. ¿En qué puedo ayudarte hoy?', 'bot');

closeBtn.addEventListener('click', () => {
  if (window.parent !== window) {
    window.parent.postMessage({ tipo: 'cerrarChatWidget' }, '*');
  }
});
