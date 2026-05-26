<template>
  <div>
    <div v-if="!isAuthenticated" class="login-page">
      <aside class="sidebar">
        <div class="logo-tag">
          <div class="logo-dot"></div>
          <span class="logo-text">Garden Sports</span>
        </div>
        <div class="sidebar-title">PANEL DE<br><span>CONTROL</span></div>
        <p class="sidebar-sub">Acceso exclusivo para administradores del sistema de reservas.</p>
        <div class="sidebar-info">
          <div class="info-row">
            <span class="info-label">Sistema</span>
            <span class="info-val">Admin <em>v1.0</em></span>
          </div>
          <div class="info-divider"></div>
          <div class="info-row">
            <span class="info-label">Estado del servidor</span>
            <span class="info-val online">Online</span>
          </div>
        </div>
        <div class="sidebar-badge">
          <strong>Acceso restringido</strong>
          Solo personal autorizado. Cualquier intento de acceso no autorizado será registrado.
        </div>
      </aside>

      <div class="login-main">
        <div class="login-box">
          <p class="login-eyebrow">Garden Sports — Admin</p>
          <div class="login-title">Iniciar sesión</div>
          <p class="login-sub">Ingresa tus credenciales para continuar al dashboard.</p>
          <form @submit.prevent="iniciarSesion">
            <div class="login-field">
              <label>Usuario</label>
              <input v-model="credenciales.username" type="text" placeholder="admin" required>
            </div>
            <div class="login-field">
              <label>Contraseña</label>
              <input v-model="credenciales.password" type="password" placeholder="" required>
            </div>
            <button type="submit" class="login-btn" :disabled="cargando">
              {{ cargando ? 'Verificando...' : 'Iniciar sesión' }}
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
        <div class="sidebar-title">PANEL DE<br><span>CONTROL</span></div>
        <p class="sidebar-sub">Gestión de reservas e instalaciones.</p>
        <div class="sidebar-info">
          <div class="info-row">
            <span class="info-label">Total reservas</span>
            <span class="info-val online">{{ reservas.length }}</span>
          </div>
          <div class="info-divider"></div>
          <div class="info-row">
            <span class="info-label">Confirmadas</span>
            <span class="info-val online">{{ contarEstado('CONFIRMADA') }}</span>
          </div>
          <div class="info-divider"></div>
          <div class="info-row">
            <span class="info-label">Pendientes</span>
            <span class="info-val">{{ contarEstado('PENDIENTE') }}</span>
          </div>
          <div class="info-divider"></div>
          <div class="info-row">
            <span class="info-label">Canceladas</span>
            <span class="info-val">{{ contarEstado('CANCELADA') }}</span>
          </div>
        </div>
        <div class="sidebar-badge">
          <strong>Sesión activa</strong>
          Recuerda cerrar sesión al terminar para proteger el acceso.
        </div>
      </aside>

      <main class="main">
        <div class="main-top">
          <div>
            <div class="main-title">ADMINISTRACIÓN</div>
            <p class="main-sub">Panel general de control y gestión de usuarios</p>
          </div>
          <div class="top-actions">
            <button class="btn-logout" @click="cerrarSesion">Cerrar sesión</button>
          </div>
        </div>

        <div class="welcome-banner">
          <h1>{{ saludoTiempo }}, <span>{{ nombreUsuario }}</span></h1>
          <p>Gestiona las reservas, monitorea las canchas y administra tus clientes.</p>
        </div>

        <div class="tabs-container">
          <div :class="['tab', { active: seccionActiva === 'monitor' }]" @click="seccionActiva = 'monitor'">
            Monitor en Vivo
          </div>
          <div :class="['tab', { active: seccionActiva === 'reservas' }]" @click="seccionActiva = 'reservas'">
            Reservaciones
          </div>
          <div :class="['tab', { active: seccionActiva === 'clientes' }]" @click="seccionActiva = 'clientes'">
            Gestión de Clientes
          </div>
        </div>

        <div v-if="seccionActiva === 'monitor'">
          <div class="monitor-grid">
            <div 
              v-for="cancha in monitorCanchas" 
              :key="cancha.id" 
              :class="['monitor-card', cancha.ocupada ? 'ocupada' : 'libre']"
            >
              <div class="monitor-header">
                <div class="monitor-type">Cancha de Pádel</div>
                <div :class="['monitor-status', cancha.ocupada ? 'status-oc' : 'status-lib']">
                  {{ cancha.ocupada ? 'EN USO' : 'LIBRE' }}
                </div>
              </div>
              <div class="monitor-name">{{ cancha.nombre }}</div>
              
              <div v-if="cancha.ocupada" class="monitor-details">
                <div class="m-detail-row">
                  <span class="m-label">Cliente</span>
                  <span class="m-val">{{ cancha.cliente }}</span>
                </div>
                <div class="m-detail-row">
                  <span class="m-label">Tiempo restante</span>
                  <span class="m-val time">{{ cancha.tiempoRestante }}</span>
                </div>
              </div>
              <div v-else class="monitor-details empty-state">
                Disponible para reservación en este momento
              </div>
            </div>
          </div>
        </div>

        <div v-if="seccionActiva === 'reservas'">
          <div class="filters-row">
            <div
              v-for="f in filtros"
              :key="f.valor"
              :class="['filter-pill', { active: filtroActivo === f.valor }]"
              @click="filtroActivo = f.valor"
            >
              {{ f.etiqueta }}
            </div>
          </div>

          <div class="table-wrap">
            <div class="table-head">
              <span class="th">Cliente</span>
              <span class="th">Cancha</span>
              <span class="th">Fecha</span>
              <span class="th">Horario</span>
              <span class="th">Estado</span>
              <span class="th" style="text-align: right;">Acciones</span>
            </div>

            <div v-if="reservasFiltradas.length === 0" class="empty">
              No hay reservas con este filtro.
            </div>

            <div
              v-for="reserva in reservasFiltradas"
              :key="reserva.id"
              class="table-row"
            >
              <div>
                <div class="td-name">{{ reserva.nombre_cliente }}</div>
                <div class="td-phone">{{ reserva.telefono_cliente }}</div>
              </div>
              <div class="td-court">
                <div>{{ reserva.cancha_nombre }}</div>
              </div>
              <div class="td-date">{{ formatearFecha(reserva.fecha) }}</div>
              <div class="td-time">{{ formatearHora(reserva.hora_inicio) }} a {{ formatearHora(reserva.hora_fin) }}</div>
              <div>
                <span :class="['badge', claseEstado(reserva.estado)]">{{ reserva.estado }}</span>
              </div>
              <div class="td-actions">
                <button 
                  v-if="reserva.estado === 'PENDIENTE'" 
                  class="btn-action-confirm" 
                  @click="confirmarReservaAdmin(reserva.id)"
                  :disabled="procesandoId === reserva.id"
                >
                  {{ procesandoId === reserva.id ? '...' : 'Aprobar' }}
                </button>
                <button 
                  v-if="reserva.estado !== 'CANCELADA'" 
                  class="btn-action-cancel" 
                  @click="cancelarReserva(reserva.id)"
                  :disabled="procesandoId === reserva.id"
                >
                  {{ procesandoId === reserva.id ? '...' : 'Cancelar' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="seccionActiva === 'clientes'">
          <div class="client-form-container">
            <div class="section">
              <div class="sec-head">
                <span class="sec-num">NUEVO</span>
                <span class="sec-name">Registro de cuenta de cliente</span>
              </div>
              <form @submit.prevent="registrarCliente" class="client-form">
                <div class="fields-row">
                  <div class="field">
                    <label>Nombre Completo</label>
                    <input v-model="nuevoCliente.first_name" type="text" placeholder="Ej. Carlos Mendoza" required>
                  </div>
                  <div class="field">
                    <label>Nombre de Usuario</label>
                    <input v-model="nuevoCliente.username" type="text" placeholder="ej. carlosm" required>
                  </div>
                </div>
                <div class="fields-row" style="margin-top: 1.5rem;">
                  <div class="field">
                    <label>Teléfono</label>
                    <input v-model="nuevoCliente.telefono" type="tel" placeholder="Ej. 645 123 4567" required>
                  </div>
                  <div class="field">
                    <label>Contraseña Acceso</label>
                    <input v-model="nuevoCliente.password" type="password" placeholder="••••••••" required>
                  </div>
                </div>
                <div class="submit-area" style="margin-top: 2.5rem;">
                  <button type="submit" class="btn-main" :disabled="guardandoCliente">
                    {{ guardandoCliente ? 'Registrando...' : 'Dar de alta cliente' }}
                  </button>
                </div>
                <div v-if="mensajeCliente.texto" :class="['alert', mensajeCliente.error ? 'err' : 'ok']">
                  {{ mensajeCliente.texto }}
                </div>
              </form>
            </div>
          </div>

          <div class="table-wrap" style="margin-top: 3rem;">
            <div class="table-head client-head">
              <span class="th">Nombre del Cliente</span>
              <span class="th">Usuario</span>
              <span class="th">Teléfono</span>
              <span class="th">Estado</span>
              <span class="th" style="text-align: right;">Acciones</span>
            </div>

            <div v-if="clientes.length === 0" class="empty">
              No hay clientes registrados en el sistema.
            </div>

            <div v-for="cliente in clientes" :key="cliente.id" class="table-row client-row">
              <div class="td-name">{{ cliente.first_name }}</div>
              <div class="td-date">{{ cliente.username }}</div>
              <div class="td-phone" style="font-family: 'Bebas Neue', sans-serif; font-size: 16px; color: #A0A4B8; letter-spacing: 0.04em;">{{ cliente.telefono_display }}</div>
              <div>
                <span :class="['badge', cliente.is_active ? 'badge-ok' : 'badge-cancel']">
                  {{ cliente.is_active ? 'ACTIVO' : 'PAUSADO' }}
                </span>
              </div>
              <div class="td-actions">
                <button 
                  :class="cliente.is_active ? 'btn-action-warn' : 'btn-action-confirm'" 
                  @click="cambiarEstadoCliente(cliente)"
                  :disabled="procesandoClienteId === cliente.id"
                >
                  {{ procesandoClienteId === cliente.id ? '...' : (cliente.is_active ? 'Pausar' : 'Activar') }}
                </button>
                <button 
                  class="btn-action-cancel" 
                  @click="eliminarCliente(cliente.id)"
                  :disabled="procesandoClienteId === cliente.id"
                >
                  {{ procesandoClienteId === cliente.id ? '...' : 'Eliminar' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const isAuthenticated = ref(false)
const cargando = ref(false)
const mensajeError = ref('')
const reservas = ref([])
const clientes = ref([])
const canchasLista = ref([])
const filtroActivo = ref('TODAS')
const seccionActiva = ref('monitor')
const procesandoId = ref(null)
const procesandoClienteId = ref(null)
const guardandoCliente = ref(false)
const ahora = ref(new Date())
const nombreUsuario = ref('')
let timerInterval = null

const credenciales = ref({ username: '', password: '' })
const nuevoCliente = ref({ username: '', password: '', first_name: '', telefono: '' })
const mensajeCliente = ref({ texto: '', error: false })

const saludoTiempo = computed(() => {
  const hora = new Date().getHours()
  if (hora < 12) return 'Buenos días'
  if (hora < 19) return 'Buenas tardes'
  return 'Buenas noches'
})

const filtros = [
  { valor: 'TODAS', etiqueta: 'Todas' },
  { valor: 'CONFIRMADA', etiqueta: 'Confirmadas' },
  { valor: 'PENDIENTE', etiqueta: 'Pendientes' },
  { valor: 'CANCELADA', etiqueta: 'Canceladas' }
]

const monitorCanchas = computed(() => {
  const hoyStr = new Date(ahora.value.getTime() - (ahora.value.getTimezoneOffset() * 60000)).toISOString().split('T')[0]
  const minActual = ahora.value.getHours() * 60 + ahora.value.getMinutes()

  return canchasLista.value.map(c => {
    const activa = reservas.value.find(r => {
      if (r.estado !== 'CONFIRMADA' || r.fecha !== hoyStr) return false
      
      let inicio = parseInt(r.hora_inicio.split(':')[0]) * 60 + parseInt(r.hora_inicio.split(':')[1])
      let fin = r.hora_fin.startsWith('00:00') ? 24 * 60 : parseInt(r.hora_fin.split(':')[0]) * 60 + parseInt(r.hora_fin.split(':')[1])
      
      return r.cancha === c.id && minActual >= inicio && minActual < fin
    })

    if (activa) {
      let fin = activa.hora_fin.startsWith('00:00') ? 24 * 60 : parseInt(activa.hora_fin.split(':')[0]) * 60 + parseInt(activa.hora_fin.split(':')[1])
      let faltanMin = fin - minActual
      let horasFaltan = Math.floor(faltanMin / 60)
      let minRestantes = faltanMin % 60
      let tiempoTxt = horasFaltan > 0 ? `${horasFaltan}h ${minRestantes}m` : `${minRestantes} min`

      return { ...c, ocupada: true, cliente: activa.nombre_cliente, tiempoRestante: tiempoTxt }
    }

    return { ...c, ocupada: false, cliente: null, tiempoRestante: null }
  })
})

const reservasFiltradas = computed(() =>
  filtroActivo.value === 'TODAS'
    ? reservas.value
    : reservas.value.filter(r => r.estado === filtroActivo.value)
)

const contarEstado = (estado) => reservas.value.filter(r => r.estado === estado).length

const formatearFecha = (f) =>
  new Date(f + 'T00:00:00').toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })

const formatearHora = (h) => {
  if (h === '00:00:00') return '12:00 AM'
  const horaInt = parseInt(h.substring(0, 2))
  return horaInt > 12 ? `${horaInt - 12}:00 PM` : `${horaInt}:00 PM`
}

const claseEstado = (estado) => {
  if (estado === 'CONFIRMADA') return 'badge-ok'
  if (estado === 'PENDIENTE') return 'badge-pend'
  return 'badge-cancel'
}

const cargarDatos = async () => {
  try {
    const resReservas = await axios.get('/api/reservas/')
    reservas.value = resReservas.data.sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
    
    const resClientes = await axios.get('/api/users/')
    clientes.value = resClientes.data

    const resCanchas = await axios.get('/api/canchas/')
    canchasLista.value = resCanchas.data.canchas || resCanchas.data
  } catch (error) {
    if (error.response?.status === 401 || error.response?.status === 403) {
      cerrarSesion()
      mensajeError.value = 'Acceso denegado. Se requieren permisos de administrador.'
    }
  }
}

const confirmarReservaAdmin = async (id) => {
  procesandoId.value = id
  try {
    await axios.patch(`/api/reservas/${id}/`, { estado: 'CONFIRMADA' })
    await cargarDatos()
  } catch (error) {
    if (error.response?.status === 401 || error.response?.status === 403) cerrarSesion()
  } finally {
    procesandoId.value = null
  }
}

const cancelarReserva = async (id) => {
  const confirmar = confirm('Confirmar la cancelacion de esta reserva')
  if (!confirmar) return

  procesandoId.value = id
  try {
    await axios.patch(`/api/reservas/${id}/`, { estado: 'CANCELADA' })
    await cargarDatos()
  } catch (error) {
    if (error.response?.status === 401 || error.response?.status === 403) cerrarSesion()
  } finally {
    procesandoId.value = null
  }
}

const registrarCliente = async () => {
  guardandoCliente.value = true
  mensajeCliente.value = { texto: '', error: false }
  try {
    await axios.post('/api/users/', nuevoCliente.value)
    mensajeCliente.value = { texto: 'Cliente dado de alta exitosamente.', error: false }
    nuevoCliente.value = { username: '', password: '', first_name: '', telefono: '' }
    await cargarDatos()
  } catch (error) {
    if (error.response?.data) {
      const errores = Object.values(error.response.data).flat().join(' | ')
      mensajeCliente.value = { texto: errores, error: true }
    } else {
      mensajeCliente.value = { texto: 'Error de red al registrar cliente.', error: true }
    }
  } finally {
    guardandoCliente.value = false
  }
}

const cambiarEstadoCliente = async (cliente) => {
  procesandoClienteId.value = cliente.id
  try {
    await axios.patch(`/api/users/${cliente.id}/`, { is_active: !cliente.is_active })
    await cargarDatos()
  } catch (error) {
    if (error.response?.status === 401 || error.response?.status === 403) cerrarSesion()
  } finally {
    procesandoClienteId.value = null
  }
}

const eliminarCliente = async (id) => {
  const confirmar = confirm('¿Estás seguro de eliminar permanentemente a este cliente? Se borrará su acceso.')
  if (!confirmar) return

  procesandoClienteId.value = id
  try {
    await axios.delete(`/api/users/${id}/`)
    await cargarDatos()
  } catch (error) {
    if (error.response?.status === 401 || error.response?.status === 403) cerrarSesion()
  } finally {
    procesandoClienteId.value = null
  }
}

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const userGuardado = localStorage.getItem('admin_username')
  if (token && userGuardado) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    try {
      await axios.get('/api/users/')
      isAuthenticated.value = true
      nombreUsuario.value = userGuardado
      cargarDatos()
      timerInterval = setInterval(() => { 
        ahora.value = new Date()
        cargarDatos()
      }, 30000)
    } catch {
      cerrarSesion()
    }
  }
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

const iniciarSesion = async () => {
  cargando.value = true
  mensajeError.value = ''
  try {
    const res = await axios.post('/api/token/', credenciales.value)
    const token = res.data.access
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
    await axios.get('/api/users/')

    localStorage.setItem('access_token', token)
    localStorage.setItem('refresh_token', res.data.refresh)
    localStorage.setItem('admin_username', credenciales.value.username)
    nombreUsuario.value = credenciales.value.username
    isAuthenticated.value = true
    credenciales.value = { username: '', password: '' }
    cargarDatos()
    timerInterval = setInterval(() => { 
      ahora.value = new Date()
      cargarDatos()
    }, 30000)
  } catch (error) {
    delete axios.defaults.headers.common['Authorization']
    if (error.response?.status === 401) {
      mensajeError.value = 'Credenciales incorrectas'
    } else if (error.response?.status === 403) {
      mensajeError.value = 'Acceso denegado. Privilegios insuficientes.'
    } else {
      mensajeError.value = 'Error al conectar con el servidor.'
    }
  } finally {
    cargando.value = false
  }
}

const cerrarSesion = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('admin_username')
  delete axios.defaults.headers.common['Authorization']
  isAuthenticated.value = false
  nombreUsuario.value = ''
  reservas.value = []
  clientes.value = []
  canchasLista.value = []
  filtroActivo.value = 'TODAS'
  seccionActiva.value = 'monitor'
  if (timerInterval) clearInterval(timerInterval)
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@700;800&family=Karla:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.page, .login-page {
  background: #11131A;
  min-height: 100vh;
  font-family: 'Karla', sans-serif;
  display: grid;
  grid-template-columns: 320px 1fr;
}

.sidebar {
  background: #161922;
  border-right: 1px solid #2A2D3D;
  padding: 3rem 2.5rem;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
}

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
.info-val em { color: #C2FF00; font-style: normal; }
.info-divider { height: 1px; background: #2A2D3D; }

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
.main-title { font-family: 'Bebas Neue', sans-serif; font-size: 38px; color: #FFFFFF; letter-spacing: 0.02em; line-height: 1; }
.main-sub { font-size: 12px; color: #A0A4B8; margin-top: 4px; }
.top-actions { display: flex; gap: 8px; }

.btn-logout { background: transparent; border: 1px solid rgba(255, 80, 80, 0.2); border-radius: 8px; padding: 0.6rem 1rem; font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 800; color: #FF6060; letter-spacing: 0.16em; text-transform: uppercase; cursor: pointer; transition: background 0.15s; }
.btn-logout:hover { background: rgba(255, 80, 80, 0.06); }

.welcome-banner { margin-bottom: 3rem; padding-bottom: 1.5rem; border-bottom: 1px solid #2A2D3D; }
.welcome-banner h1 { font-family: 'Bebas Neue', sans-serif; font-size: 42px; color: #FFFFFF; letter-spacing: 0.02em; font-weight: normal; line-height: 1; }
.welcome-banner h1 span { color: #C2FF00; }
.welcome-banner p { font-family: 'Karla', sans-serif; font-size: 14px; color: #A0A4B8; margin-top: 8px; }

.tabs-container { display: flex; gap: 1rem; margin-bottom: 2.5rem; border-bottom: 1px solid #2A2D3D; padding-bottom: 1px; }
.tab { font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 800; color: #5A5E70; letter-spacing: 0.18em; text-transform: uppercase; padding: 0.8rem 1.5rem; cursor: pointer; transition: all 0.2s; border-bottom: 2px solid transparent; margin-bottom: -1px; }
.tab:hover { color: #A0A4B8; }
.tab.active { color: #C2FF00; border-bottom: 2px solid #C2FF00; }

.monitor-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
.monitor-card { background: #161922; border: 1px solid #2A2D3D; border-radius: 12px; padding: 1.5rem; transition: all 0.2s; }
.monitor-card.ocupada { border-color: #C2FF00; background: #1A1D28; }
.monitor-card.libre { border-color: #3A3D50; opacity: 0.8; }
.monitor-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.monitor-type { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.18em; text-transform: uppercase; }
.monitor-status { font-family: 'Syne', sans-serif; font-size: 8px; font-weight: 800; letter-spacing: 0.1em; padding: 3px 8px; border-radius: 4px; }
.status-oc { background: rgba(194,255,0,0.1); color: #C2FF00; }
.status-lib { background: rgba(138,142,155,0.1); color: #8A8E9B; }
.monitor-name { font-family: 'Bebas Neue', sans-serif; font-size: 32px; color: #FFFFFF; letter-spacing: 0.04em; margin-bottom: 1.5rem; }
.monitor-details { border-top: 1px solid #2A2D3D; padding-top: 1.2rem; }
.m-detail-row { display: flex; flex-direction: column; gap: 4px; margin-bottom: 1rem; }
.m-detail-row:last-child { margin-bottom: 0; }
.m-label { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.1em; text-transform: uppercase; }
.m-val { font-family: 'Karla', sans-serif; font-size: 15px; color: #FFFFFF; font-weight: 600; }
.m-val.time { color: #C2FF00; }
.empty-state { font-size: 12px; color: #5A5E70; font-family: 'Karla', sans-serif; font-style: italic; }

.filters-row { display: flex; gap: 8px; margin-bottom: 1.5rem; }
.filter-pill { background: #161922; border: 1px solid #2A2D3D; border-radius: 6px; padding: 0.4rem 0.9rem; font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.14em; text-transform: uppercase; cursor: pointer; transition: border-color 0.15s, color 0.15s; }
.filter-pill.active { border-color: #C2FF00; color: #C2FF00; }

.table-wrap { background: #161922; border: 1px solid #2A2D3D; border-radius: 12px; overflow: hidden; }
.table-head { display: grid; grid-template-columns: 2fr 1.6fr 1.2fr 1.2fr 1fr 1.4fr; padding: 0.9rem 1.5rem; border-bottom: 1px solid #2A2D3D; }
.client-head { grid-template-columns: 2fr 1.5fr 2fr 1fr 1.5fr; }
.th { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.18em; text-transform: uppercase; }
.table-row { display: grid; grid-template-columns: 2fr 1.6fr 1.2fr 1.2fr 1fr 1.4fr; padding: 1rem 1.5rem; border-bottom: 1px solid #2A2D3D; transition: background 0.15s; align-items: center; }
.client-row { grid-template-columns: 2fr 1.5fr 2fr 1fr 1.5fr; }
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: #1A1D28; }
.td-name { font-family: 'Karla', sans-serif; font-size: 14px; color: #FFFFFF; font-weight: 600; }
.td-phone { font-family: 'Karla', sans-serif; font-size: 11px; color: #A0A4B8; margin-top: 2px; }
.td-court { font-family: 'Bebas Neue', sans-serif; font-size: 18px; color: #A0A4B8; letter-spacing: 0.04em; }
.td-date { font-family: 'Karla', sans-serif; font-size: 13px; color: #A0A4B8; }
.td-time { font-family: 'Bebas Neue', sans-serif; font-size: 16px; color: #A0A4B8; letter-spacing: 0.04em; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 4px; font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
.badge-ok { background: rgba(194,255,0,0.08); border: 1px solid rgba(194,255,0,0.2); color: #C2FF00; }
.badge-pend { background: rgba(255,180,0,0.08); border: 1px solid rgba(255,180,0,0.2); color: #FFB400; }
.badge-cancel { background: rgba(255,80,80,0.08); border: 1px solid rgba(255,80,80,0.2); color: #FF6060; }

.td-actions { display: flex; justify-content: flex-end; gap: 6px; }
.btn-action-confirm { background: transparent; border: 1px solid rgba(194, 255, 0, 0.4); border-radius: 6px; padding: 0.4rem 0.8rem; font-family: 'Syne', sans-serif; font-size: 8px; font-weight: 800; color: #C2FF00; letter-spacing: 0.1em; text-transform: uppercase; cursor: pointer; transition: all 0.15s; }
.btn-action-confirm:hover { background: rgba(194, 255, 0, 0.1); border-color: #C2FF00; }
.btn-action-confirm:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-action-warn { background: transparent; border: 1px solid rgba(255, 180, 0, 0.4); border-radius: 6px; padding: 0.4rem 0.8rem; font-family: 'Syne', sans-serif; font-size: 8px; font-weight: 800; color: #FFB400; letter-spacing: 0.1em; text-transform: uppercase; cursor: pointer; transition: all 0.15s; }
.btn-action-warn:hover { background: rgba(255, 180, 0, 0.1); border-color: #FFB400; }
.btn-action-warn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-action-cancel { background: transparent; border: 1px solid rgba(255, 96, 96, 0.4); border-radius: 6px; padding: 0.4rem 0.8rem; font-family: 'Syne', sans-serif; font-size: 8px; font-weight: 800; color: #FF6060; letter-spacing: 0.1em; text-transform: uppercase; cursor: pointer; transition: all 0.15s; }
.btn-action-cancel:hover { background: rgba(255, 96, 96, 0.1); border-color: #FF6060; }
.btn-action-cancel:disabled { opacity: 0.5; cursor: not-allowed; }

.client-form-container { background: #161922; border: 1px solid #2A2D3D; border-radius: 10px; padding: 2.5rem; }
.client-form { margin-top: 2rem; }
.section { margin-bottom: 0; }
.sec-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #2A2D3D; }
.sec-num { font-family: 'Bebas Neue', sans-serif; font-size: 38px; color: #4A4E69; line-height: 1; }
.sec-name { font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 800; color: #A0A4B8; letter-spacing: 0.22em; text-transform: uppercase; }
.fields-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.field { display: flex; flex-direction: column; gap: 8px; }
.field label { font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700; color: #8A8E9B; letter-spacing: 0.2em; text-transform: uppercase; }
.field input { background: transparent; border: none; border-bottom: 1px solid #3A3D50; padding: 0.6rem 0; font-family: 'Karla', sans-serif; font-size: 15px; color: #FFFFFF; outline: none; transition: border-color 0.15s; width: 100%; }
.field input:focus { border-color: #C2FF00; }
.field input::placeholder { color: #5A5E70; }

.submit-area { display: grid; grid-template-columns: 1fr; gap: 10px; }
.btn-main { background: #C2FF00; color: #080A0C; font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; border: none; border-radius: 10px; padding: 1rem 2rem; cursor: pointer; transition: background 0.15s; width: max-content; }
.btn-main:hover { background: #D0FF33; }
.btn-main:disabled { background: #2A2D3D; color: #5A5E70; cursor: not-allowed; }

.alert { padding: 0.9rem 1.2rem; border-radius: 8px; font-size: 13px; font-weight: 600; text-align: center; margin-top: 1.5rem; font-family: 'Karla', sans-serif; }
.alert.ok { background: rgba(194,255,0,0.07); border: 1px solid rgba(194,255,0,0.2); color: #C2FF00; }
.alert.err { background: rgba(255,80,80,0.07); border: 1px solid rgba(255,80,80,0.2); color: #FF7070; }
.empty { padding: 3rem; text-align: center; font-size: 13px; color: #8A8E9B; font-family: 'Karla', sans-serif; }

@media (max-width: 768px) {
  .page, .login-page { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; padding: 2rem 1.5rem; }
  .sidebar-title { font-size: 40px; }
  .main { padding: 2rem 1.5rem; }
  .login-main { padding: 2rem 1.5rem; }
  .table-head, .table-row, .fields-row, .monitor-grid { grid-template-columns: 1fr; }
  .th:nth-child(n+3), .table-row > div:nth-child(n+3) { display: none; }
  .filters-row { flex-wrap: wrap; }
  .btn-main { width: 100%; }
}
</style>