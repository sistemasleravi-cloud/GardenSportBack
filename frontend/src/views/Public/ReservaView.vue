<template>
  <div>
    <div v-if="!isAuthenticated" class="login-page">
      <aside class="sidebar">
        <div class="logo-tag">
          <div class="logo-dot"></div>
          <span class="logo-text">Garden Sports</span>
        </div>
        <div class="sidebar-title">PORTAL DE<br><span>CLIENTES</span></div>
        <p class="sidebar-sub">Inicia sesión con tu cuenta para agendar tu cancha.</p>
        <div class="sidebar-info">
          <div class="info-row">
            <span class="info-label">Acceso</span>
            <span class="info-val">Exclusivo</span>
          </div>
          <div class="info-divider"></div>
          <div class="info-row">
            <span class="info-label">Estado</span>
            <span class="info-val online">Activo</span>
          </div>
        </div>
        <div class="sidebar-badge">
          <strong>¿No tienes cuenta?</strong>
          <a href="https://wa.me/526453406382" target="_blank" style="color: #C2FF00; text-decoration: underline;">
            Comunícate con la administración de Garden Sports por Whatsapp
          </a> 
          para darte de alta en el sistema.
        </div>
      </aside>

      <div class="login-main">
        <div class="login-box">
          <p class="login-eyebrow">Garden Sports — Reservas</p>
          <div class="login-title">Iniciar sesión</div>
          <p class="login-sub">Ingresa tu usuario y contraseña para acceder al calendario.</p>
          <form @submit.prevent="iniciarSesion">
            <div class="login-field">
              <label>Usuario</label>
              <input v-model="credenciales.username" type="text" placeholder="" required>
            </div>
            <div class="login-field">
              <label>Contraseña</label>
              <input v-model="credenciales.password" type="password" placeholder="" required>
            </div>
            <button type="submit" class="login-btn" :disabled="cargandoLogin">
              {{ cargandoLogin ? 'Verificando...' : 'Iniciar sesión' }}
            </button>
          </form>
          <div v-if="mensajeError" class="login-err">{{ mensajeError }}</div>
        </div>
      </div>
    </div>

    <div v-else class="page">
      <aside class="sidebar">
        <div class="logo-tag">
          <div class="logo-dot"></div>
          <span class="logo-text">Garden Sports</span>
        </div>
        <div class="sidebar-title">AGENDA<br>TU <span>CANCHA</span></div>
        <p class="sidebar-sub">Elige el horario y confirma tu espacio.</p>
        <div class="sidebar-steps">
          <div :class="['s-step', { active: pasoActivo >= 1, done: pasoActivo > 1 }]">
            <span class="s-num">01</span><span class="s-label">Fecha y horario</span>
          </div>
          <div class="s-line"></div>
          <div :class="['s-step', { active: pasoActivo >= 2 }]">
            <span class="s-num">02</span><span class="s-label">Selección de cancha</span>
          </div>
        </div>
        <div class="sidebar-badge">
          <strong>Horario de atención</strong>
          Lun – Dom: 4:00 pm – 12:00 am<br>
          Reservas con mínimo 1 hora de anticipación.
        </div>
      </aside>

      <main class="main">
        <div class="main-top">
          <div class="top-right"><span>RESERVACIONES 2026</span></div>
          <div class="top-user-actions">
            <button class="btn-logout" @click="cerrarSesion">Cerrar sesión</button>
          </div>
        </div>

        <div class="welcome-banner">
          <h1>{{ saludoTiempo }}, <span>{{ nombreUsuario }}</span></h1>
          <p>Selecciona la fecha y el horario para verificar la disponibilidad de nuestras canchas.</p>
        </div>

        <form @submit.prevent="confirmarReserva">
          <div class="section">
            <div class="sec-head">
              <span class="sec-num">01</span>
              <span class="sec-name">Fecha y horario</span>
            </div>
            <div class="fields-row">
              <div class="field">
                <label>Fecha</label>
                <input v-model="reserva.fecha" type="date" required @change="resetCanchas">
              </div>
            </div>
            <div class="time-row">
              <div class="field">
                <label>Hora de entrada</label>
                <select v-model="reserva.hora_inicio" required @change="resetCanchas" class="field-select">
                  <option value="" disabled>Seleccionar hora</option>
                  <option v-for="hora in horasDisponibles" :key="hora" :value="hora">
                    {{ formatearHoraVista(hora) }}
                  </option>
                </select>
              </div>
              <div class="time-sep">→</div>
              <div class="field">
                <label>Hora de salida</label>
                <select v-model="reserva.hora_fin" required @change="resetCanchas" class="field-select">
                  <option value="" disabled>Seleccionar hora</option>
                  <option v-for="hora in horasDisponiblesSalida" :key="hora" :value="hora">
                    {{ formatearHoraVista(hora) }}
                  </option>
                </select>
              </div>
            </div>
            <button type="button" class="check-btn" :disabled="verificando" @click="verificarDisponibilidad">
              {{ verificando ? 'Consultando...' : 'Verificar disponibilidad' }}
            </button>
          </div>

          <div class="section">
            <div class="sec-head">
              <span class="sec-num">02</span>
              <span class="sec-name">Selección de cancha</span>
            </div>
            <div class="court-grid">
              <div v-if="!disponibilidadVerified" class="court-hint">
                Completa el horario y verifica disponibilidad para ver las canchas.
              </div>
              <template v-else>
                <div
                  v-for="c in canchasMostradas"
                  :key="c.id"
                  :class="['court-card', {
                    active: reserva.cancha === c.id,
                    unavailable: !c.disponible && c.activa,
                    inactive: !c.activa
                  }]"
                  @click="c.disponible && c.activa && (reserva.cancha = c.id)"
                >
                  <div class="court-dot"></div>
                  <div class="court-type">Cancha</div>
                  <div class="court-name">{{ c.nombre }}</div>
                  <div class="court-avail">{{ estadoTexto(c) }}</div>
                </div>
                <div v-if="canchasMostradas.length === 0" class="court-hint">
                  No hay canchas registradas en el sistema.
                </div>
              </template>
            </div>
          </div>

          <div class="submit-area">
            <button type="submit" class="btn-main" :disabled="cargando || !reserva.cancha">
              {{ cargando ? 'Procesando...' : 'Confirmar Reserva' }}
            </button>
            <button type="button" class="btn-clear" @click="limpiarFormulario">Limpiar</button>
          </div>

          <div v-if="mensaje.texto" :class="['alert', mensaje.error ? 'err' : 'ok']">
            {{ mensaje.texto }}
          </div>
        </form>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const isAuthenticated = ref(false)
const cargandoLogin = ref(false)
const mensajeError = ref('')
const credenciales = ref({ username: '', password: '' })
const nombreUsuario = ref('')

const canchas = ref([])
const canchasOcupadas = ref([])
const cargando = ref(false)
const verificando = ref(false)
const disponibilidadVerified = ref(false)
const pasoActivo = ref(1)
const mensaje = ref({ texto: '', error: false })

const reserva = ref({
  cancha: null,
  nombre_cliente: '',
  telefono_cliente: '',
  fecha: '',
  hora_inicio: '',
  hora_fin: '',
  estado: 'CONFIRMADA'
})

const horasDisponibles = ['16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
const horasDisponiblesSalida = ['17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '00:00']

const saludoTiempo = computed(() => {
  const hora = new Date().getHours()
  if (hora < 12) return 'Buenos días'
  if (hora < 19) return 'Buenas tardes'
  return 'Buenas noches'
})

onMounted(() => {
  const token = localStorage.getItem('access_token_cliente')
  const userGuardado = localStorage.getItem('cliente_username')
  if (token && userGuardado) {
    isAuthenticated.value = true
    nombreUsuario.value = userGuardado
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
})

const iniciarSesion = async () => {
  cargandoLogin.value = true
  mensajeError.value = ''
  try {
    const res = await axios.post('/api/token/', credenciales.value)
    const token = res.data.access
    localStorage.setItem('access_token_cliente', token)
    localStorage.setItem('refresh_token_cliente', res.data.refresh)
    localStorage.setItem('cliente_username', credenciales.value.username)
    nombreUsuario.value = credenciales.value.username
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    isAuthenticated.value = true
    credenciales.value = { username: '', password: '' }
  } catch {
    mensajeError.value = 'Credenciales incorrectas'
  } finally {
    cargandoLogin.value = false
  }
}

const cerrarSesion = () => {
  localStorage.removeItem('access_token_cliente')
  localStorage.removeItem('refresh_token_cliente')
  localStorage.removeItem('cliente_username')
  delete axios.defaults.headers.common['Authorization']
  isAuthenticated.value = false
  nombreUsuario.value = ''
  limpiarFormularioBase()
}

const formatearHoraVista = (hora) => {
  if (hora === '00:00') return '12:00 AM'
  const h = parseInt(hora.split(':')[0])
  return h > 12 ? `${h - 12}:00 PM` : `${h}:00 PM`
}

const canchasMostradas = computed(() => {
  return canchas.value.map(c => ({
    ...c,
    disponible: !canchasOcupadas.value.includes(c.id)
  }))
})

const estadoTexto = (c) => {
  if (!c.activa) return 'En mantenimiento'
  if (!c.disponible) return 'No disponible'
  return 'Disponible'
}

const resetCanchas = () => {
  reserva.value.cancha = null
  canchasOcupadas.value = []
  disponibilidadVerified.value = false
  pasoActivo.value = 1
  mensaje.value = { texto: '', error: false }
}

const verificarDisponibilidad = async () => {
  if (!reserva.value.fecha || !reserva.value.hora_inicio || !reserva.value.hora_fin) {
    mensaje.value = { texto: 'Ingresa fecha, hora de entrada y hora de salida.', error: true }
    return
  }

  const finAjustado = reserva.value.hora_fin === '00:00' ? '24:00' : reserva.value.hora_fin
  
  if (reserva.value.hora_inicio >= finAjustado) {
    mensaje.value = { texto: 'La hora de salida debe ser mayor a la de entrada.', error: true }
    return
  }

  verificando.value = true
  mensaje.value = { texto: '', error: false }

  try {
    const res = await axios.get('/api/canchas/', {
      params: {
        fecha: reserva.value.fecha,
        hora_inicio: reserva.value.hora_inicio,
        hora_fin: reserva.value.hora_fin
      }
    })
    canchas.value = res.data.canchas ? res.data.canchas : res.data
    canchasOcupadas.value = res.data.ocupadas || []
    disponibilidadVerified.value = true
    pasoActivo.value = 2
  } catch (error) {
    if (error.response?.status === 401) cerrarSesion()
    mensaje.value = { texto: 'Error al consultar disponibilidad.', error: true }
  } finally {
    verificando.value = false
  }
}

const confirmarReserva = async () => {
  cargando.value = true
  mensaje.value = { texto: '', error: false }
  
  reserva.value.nombre_cliente = nombreUsuario.value
  reserva.value.telefono_cliente = 'Cuenta Registrada'

  try {
    await axios.post('/api/reservas/', reserva.value)
    mensaje.value = { texto: 'Reserva confirmada. Nos vemos pronto.', error: false }
    limpiarFormularioBase()
    setTimeout(() => { mensaje.value.texto = '' }, 5000)
  } catch (error) {
    if (error.response?.status === 401) cerrarSesion()
    if (error.response?.data) {
      const errores = Object.values(error.response.data).flat().join(' | ')
      mensaje.value = { texto: errores, error: true }
    } else {
      mensaje.value = { texto: 'Ocurrió un error inesperado de red.', error: true }
    }
  } finally {
    cargando.value = false
  }
}

const limpiarFormularioBase = () => {
  reserva.value.cancha = null
  reserva.value.nombre_cliente = ''
  reserva.value.telefono_cliente = ''
  reserva.value.fecha = ''
  reserva.value.hora_inicio = ''
  reserva.value.hora_fin = ''
  reserva.value.estado = 'CONFIRMADA'
  canchasOcupadas.value = []
  disponibilidadVerified.value = false
  pasoActivo.value = 1
}

const limpiarFormulario = () => {
  limpiarFormularioBase()
  mensaje.value = { texto: '', error: false }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@700;800&family=Karla:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.page, .login-page { background: #11131A; min-height: 100vh; font-family: 'Karla', sans-serif; display: grid; grid-template-columns: 320px 1fr; }
.sidebar { background: #161922; border-right: 1px solid #2A2D3D; padding: 3rem 2.5rem; display: flex; flex-direction: column; position: sticky; top: 0; height: 100vh; }
.logo-tag { display: flex; align-items: center; gap: 10px; margin-bottom: 3rem; }
.logo-dot { width: 8px; height: 8px; background: #C2FF00; border-radius: 50%; }
.logo-text { font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 800; color: #C2FF00; letter-spacing: 0.18em; text-transform: uppercase; }

.sidebar-title { font-family: 'Bebas Neue', sans-serif; font-size: 52px; color: #FFFFFF; line-height: 0.88; letter-spacing: 0.02em; margin-bottom: 1rem; }
.sidebar-title span { color: #C2FF00; }
.sidebar-sub { font-size: 12px; color: #A0A4B8; line-height: 1.6; margin-bottom: 3rem; }
.sidebar-info { display: flex; flex-direction: column; gap: 1rem; margin-bottom: auto; }
.info-row { display: flex; flex-direction: column; gap: 4px; }
.info-label { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.2em; text-transform: uppercase; }
.info-val { font-family: 'Bebas Neue', sans-serif; font-size: 28px; color: #FFFFFF; letter-spacing: 0.04em; line-height: 1; }
.info-val.online { color: #C2FF00; }
.info-divider { height: 1px; background: #2A2D3D; }

.sidebar-steps { display: flex; flex-direction: column; gap: 1.2rem; margin-bottom: auto; }
.s-step { display: flex; align-items: center; gap: 12px; opacity: 0.35; transition: opacity 0.2s; }
.s-step.active { opacity: 1; }
.s-step.done { opacity: 0.65; }
.s-num { font-family: 'Bebas Neue', sans-serif; font-size: 13px; color: #C2FF00; width: 20px; }
.s-label { font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 700; color: #A0A4B8; letter-spacing: 0.16em; text-transform: uppercase; }
.s-line { width: 1px; height: 20px; background: #2A2D3D; margin-left: 9px; }

.sidebar-badge { margin-top: 3rem; background: #1A1D28; border: 1px solid #2A2D3D; border-radius: 8px; padding: 1rem; font-size: 11px; color: #A0A4B8; line-height: 1.5; }
.sidebar-badge strong { color: #C2FF00; display: block; font-family: 'Syne', sans-serif; font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 4px; }

.login-main { display: flex; align-items: center; justify-content: center; padding: 3rem; }
.login-box { width: 100%; max-width: 380px; }
.login-eyebrow { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.5rem; }
.login-title { font-family: 'Bebas Neue', sans-serif; font-size: 42px; color: #FFFFFF; letter-spacing: 0.02em; margin-bottom: 0.5rem; }
.login-sub { font-size: 12px; color: #A0A4B8; margin-bottom: 2.5rem; }
.login-field { display: flex; flex-direction: column; gap: 8px; margin-bottom: 1.5rem; }
.login-field label { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.2em; text-transform: uppercase; }
.login-field input { background: transparent; border: 1px solid #3A3D50; border-radius: 8px; padding: 0.75rem 1rem; font-family: 'Karla', sans-serif; font-size: 15px; color: #FFFFFF; outline: none; transition: border-color 0.15s; width: 100%; }
.login-field input:focus { border-color: #C2FF00; }
.login-btn { width: 100%; padding: 0.9rem; background: #C2FF00; color: #080A0C; font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; border: none; border-radius: 8px; cursor: pointer; margin-top: 0.5rem; transition: background 0.15s; }
.login-btn:hover { background: #D0FF33; }
.login-btn:disabled { background: #2A2D3D; color: #5A5E70; cursor: not-allowed; }
.login-err { background: rgba(255, 80, 80, 0.07); border: 1px solid rgba(255, 80, 80, 0.2); color: #FF7070; padding: 0.8rem 1rem; border-radius: 8px; font-size: 12px; font-weight: 600; text-align: center; margin-top: 1rem; }

.main { padding: 3rem 3.5rem; overflow-y: auto; }
.main-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 2rem; }
.top-right span { font-family: 'Bebas Neue', sans-serif; font-size: 12px; color: #5A5E70; letter-spacing: 0.1em; }
.top-user-actions { display: flex; align-items: center; gap: 1.5rem; }
.btn-logout { background: transparent; border: 1px solid rgba(255, 80, 80, 0.2); border-radius: 8px; padding: 0.6rem 1rem; font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 800; color: #FF6060; letter-spacing: 0.16em; text-transform: uppercase; cursor: pointer; transition: background 0.15s; }
.btn-logout:hover { background: rgba(255, 80, 80, 0.06); }

.welcome-banner { margin-bottom: 3rem; padding-bottom: 1.5rem; border-bottom: 1px solid #2A2D3D; }
.welcome-banner h1 { font-family: 'Bebas Neue', sans-serif; font-size: 42px; color: #FFFFFF; letter-spacing: 0.02em; font-weight: normal; line-height: 1; }
.welcome-banner h1 span { color: #C2FF00; }
.welcome-banner p { font-family: 'Karla', sans-serif; font-size: 14px; color: #A0A4B8; margin-top: 8px; }

.section { margin-bottom: 3rem; }
.sec-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #2A2D3D; }
.sec-num { font-family: 'Bebas Neue', sans-serif; font-size: 38px; color: #4A4E69; line-height: 1; }
.sec-name { font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 800; color: #A0A4B8; letter-spacing: 0.22em; text-transform: uppercase; }
.fields-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.field { display: flex; flex-direction: column; gap: 8px; }
.field label { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.2em; text-transform: uppercase; }
.field input, .field-select { background: #11131A; border: none; border-bottom: 1px solid #3A3D50; padding: 0.6rem 0; font-family: 'Karla', sans-serif; font-size: 15px; color: #FFFFFF; outline: none; transition: border-color 0.15s; width: 100%; }
.field input:focus, .field-select:focus { border-color: #C2FF00; }
.field-select { cursor: pointer; }
.field-select option { background: #161922; color: #FFFFFF; }
.time-row { display: grid; grid-template-columns: 1fr 40px 1fr; align-items: end; gap: 0.5rem; margin-top: 1.5rem; }
.time-sep { font-family: 'Bebas Neue', sans-serif; font-size: 22px; color: #5A5E70; text-align: center; padding-bottom: 0.5rem; }
.check-btn { width: 100%; margin-top: 1.5rem; padding: 0.8rem; background: transparent; border: 1px solid #C2FF00; border-radius: 8px; font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 800; color: #C2FF00; letter-spacing: 0.18em; text-transform: uppercase; cursor: pointer; transition: background 0.15s; }
.check-btn:hover { background: rgba(194, 255, 0, 0.06); }
.check-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.court-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.court-hint { font-size: 12px; color: #A0A4B8; padding: 1.5rem; text-align: center; border: 1px dashed #3A3D50; border-radius: 10px; grid-column: 1 / -1; font-family: 'Karla', sans-serif; }
.court-card { background: #161922; border: 1px solid #2A2D3D; border-radius: 10px; padding: 1.1rem 1.2rem; cursor: pointer; transition: border-color 0.15s, background 0.15s; position: relative; user-select: none; display: block; }
.court-card:hover:not(.unavailable):not(.inactive) { border-color: #4A4E69; background: #1A1D28; }
.court-card.active { border-color: #C2FF00; background: #1A1D28; }
.court-card.unavailable { opacity: 0.45; cursor: not-allowed; pointer-events: none; }
.court-card.inactive { opacity: 0.35; cursor: not-allowed; pointer-events: none; }
.court-dot { width: 6px; height: 6px; border-radius: 50%; background: #3A3D50; position: absolute; top: 14px; right: 14px; transition: background 0.15s; }
.court-card.active .court-dot { background: #C2FF00; }
.court-card.unavailable .court-dot { background: #FF4444; }
.court-type { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 4px; }
.court-name { font-family: 'Bebas Neue', sans-serif; font-size: 22px; color: #FFFFFF; letter-spacing: 0.04em; }
.court-avail { font-size: 11px; color: #8A8E9B; margin-top: 3px; font-family: 'Karla', sans-serif; }
.court-card.active .court-avail { color: #8BCC00; }
.court-card.unavailable .court-avail { color: #FF6060; }

.submit-area { display: grid; grid-template-columns: 1fr auto; gap: 10px; margin-top: 2.5rem; }
.btn-main { background: #C2FF00; color: #080A0C; font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; border: none; border-radius: 10px; padding: 1rem 2rem; cursor: pointer; transition: background 0.15s; }
.btn-main:hover { background: #D0FF33; }
.btn-main:disabled { background: #2A2D3D; color: #5A5E70; cursor: not-allowed; }
.btn-clear { background: transparent; border: 1px solid #3A3D50; border-radius: 10px; padding: 1rem 1.2rem; cursor: pointer; transition: border-color 0.15s, color 0.15s; font-family: 'Karla', sans-serif; font-size: 13px; color: #8A8E9B; white-space: nowrap; }
.btn-clear:hover { border-color: #5A5E70; color: #FFFFFF; }

.alert { padding: 0.9rem 1.2rem; border-radius: 8px; font-size: 13px; font-weight: 600; text-align: center; margin-top: 1rem; font-family: 'Karla', sans-serif; }
.alert.ok { background: rgba(194,255,0,0.07); border: 1px solid rgba(194,255,0,0.2); color: #C2FF00; }
.alert.err { background: rgba(255,80,80,0.07); border: 1px solid rgba(255,80,80,0.2); color: #FF7070; }

@media (max-width: 768px) {
  .page, .login-page { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; padding: 2rem 1.5rem; }
  .sidebar-title { font-size: 42px; }
  .main { padding: 2rem 1.5rem; }
  .login-main { padding: 2rem 1.5rem; }
  .fields-row, .court-grid { grid-template-columns: 1fr; }
  .time-row { grid-template-columns: 1fr; }
  .time-sep { display: none; }
  .submit-area { grid-template-columns: 1fr; }
  .top-user-actions { flex-direction: column; align-items: flex-end; gap: 0.8rem; }
}
</style>
