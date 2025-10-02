<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <div class="w-64 bg-gray-900 text-white fixed inset-y-0 left-0 transform transition-transform duration-300 ease-in-out z-50" :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'">
      <!-- Logo -->
      <div class="flex items-center justify-center h-16 bg-yellow-400 text-black">
        <h1 class="text-xl font-bold">SmartNet</h1>
      </div>
      
      <!-- Navigation -->
      <nav class="mt-8">
        <div class="px-4 space-y-2">
          <nuxt-link 
            to="/" 
            class="sidebar-item group"
            :class="{ 'active': $route.path === '/' }"
          >
            <Icon name="heroicons:home" class="w-5 h-5 mr-3" />
            Dashboard
          </nuxt-link>
          
          <nuxt-link 
            to="/usage" 
            class="sidebar-item group"
            :class="{ 'active': $route.path === '/usage' }"
          >
            <Icon name="heroicons:chart-bar" class="w-5 h-5 mr-3" />
            Kullanım Takibi
          </nuxt-link>
          
          <nuxt-link 
            to="/plans" 
            class="sidebar-item group"
            :class="{ 'active': $route.path === '/plans' }"
          >
            <Icon name="heroicons:wifi" class="w-5 h-5 mr-3" />
            Paket Yönetimi
          </nuxt-link>
          
          <nuxt-link 
            to="/address-search" 
            class="sidebar-item group"
            :class="{ 'active': $route.path === '/address-search' }"
          >
            <Icon name="heroicons:map-pin" class="w-5 h-5 mr-3" />
            Adres Sorgulama
          </nuxt-link>
          
          <nuxt-link 
            to="/support" 
            class="sidebar-item group"
            :class="{ 'active': $route.path === '/support' }"
          >
            <Icon name="heroicons:ticket" class="w-5 h-5 mr-3" />
            Destek
          </nuxt-link>
        </div>
        
        <!-- Kullanıcı Bilgileri -->
        <div class="mt-8 px-4">
          <div class="bg-gray-800 rounded-lg p-4">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center text-black font-semibold">
                M
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium">Müşteri</p>
                <p class="text-xs text-gray-400">Fiber 100 Mbps</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Hızlı Aksiyonlar -->
        <div class="mt-6 px-4">
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Hızlı Aksiyonlar</h3>
          <div class="space-y-2">
            <button @click="resetModem" class="w-full text-left sidebar-item">
              <Icon name="heroicons:arrow-path" class="w-5 h-5 mr-3" />
              Modem Reset
            </button>
            <button @click="reportIssue" class="w-full text-left sidebar-item">
              <Icon name="heroicons:exclamation-triangle" class="w-5 h-5 mr-3" />
              Arıza Bildir
            </button>
            <button @click="openLiveChat" class="w-full text-left sidebar-item">
              <Icon name="heroicons:chat-bubble-left-right" class="w-5 h-5 mr-3" />
              Canlı Destek
            </button>
          </div>
        </div>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 lg:ml-64">
      <!-- Mobile Header -->
      <div class="lg:hidden bg-white shadow-sm border-b border-gray-200">
        <div class="flex items-center justify-between px-4 py-3">
          <button @click="sidebarOpen = !sidebarOpen" class="text-gray-600 hover:text-gray-900">
            <Icon name="heroicons:bars-3" class="w-6 h-6" />
          </button>
          <h1 class="text-lg font-semibold text-gray-900">SmartNet</h1>
          <div class="w-6"></div>
        </div>
      </div>

      <!-- Page Content -->
      <main class="p-6">
        <slot />
      </main>
    </div>

    <!-- Mobile Sidebar Overlay -->
    <div 
      v-if="sidebarOpen" 
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
    ></div>

    <!-- Live Chat Popup -->
    <div v-if="chatOpen" class="chat-popup">
      <div class="chat-header">
        <span>Canlı Destek</span>
        <button @click="chatOpen = false" class="text-black hover:text-gray-700">
          <Icon name="heroicons:x-mark" class="w-5 h-5" />
        </button>
      </div>
      
      <div class="chat-messages">
        <div v-for="message in chatMessages" :key="message.id" class="mb-3">
          <div class="flex" :class="message.sender === 'user' ? 'justify-end' : 'justify-start'">
            <div 
              class="max-w-xs px-3 py-2 rounded-lg text-sm"
              :class="message.sender === 'user' ? 'bg-yellow-400 text-black' : 'bg-gray-200 text-gray-800'"
            >
              {{ message.text }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <div class="flex space-x-2">
          <input 
            v-model="newMessage"
            @keypress.enter="sendMessage"
            type="text" 
            placeholder="Mesajınızı yazın..."
            class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 text-sm"
          >
          <button @click="sendMessage" class="bg-yellow-400 text-black px-3 py-2 rounded-lg hover:bg-yellow-500">
            <Icon name="heroicons:paper-airplane" class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- Floating Chat Button -->
    <button 
      v-if="!chatOpen"
      @click="openLiveChat"
      class="fixed bottom-6 right-6 w-14 h-14 bg-yellow-400 text-black rounded-full shadow-lg hover:bg-yellow-500 transition-colors z-40 flex items-center justify-center"
    >
      <Icon name="heroicons:chat-bubble-left-right" class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup>
// API config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Reactive state
const sidebarOpen = ref(false)
const chatOpen = ref(false)
const newMessage = ref('')
const chatMessages = ref([
  {
    id: 1,
    sender: 'support',
    text: 'Merhaba! Size nasıl yardımcı olabilirim?'
  }
])

// Methods
const resetModem = async () => {
  try {
    const response = await $fetch(`${apiBase}/support/reset-modem`, {
      method: 'POST',
      body: { user_id: 'U1' }
    })
    alert('Modem sıfırlama komutu gönderildi! 2-3 dakika içinde modem yeniden başlayacak.')
  } catch (error) {
    alert('Modem sıfırlama işlemi başarısız oldu. Lütfen tekrar deneyin.')
  }
}

const reportIssue = () => {
  navigateTo('/support?action=report')
}

const openLiveChat = () => {
  chatOpen.value = true
}

const sendMessage = () => {
  if (!newMessage.value.trim()) return
  
  // Kullanıcı mesajını ekle
  chatMessages.value.push({
    id: Date.now(),
    sender: 'user',
    text: newMessage.value
  })
  
  // Otomatik yanıt simülasyonu
  setTimeout(() => {
    chatMessages.value.push({
      id: Date.now() + 1,
      sender: 'support',
      text: 'Mesajınız alındı. Bir temsilcimiz en kısa sürede size dönüş yapacak.'
    })
  }, 1000)
  
  newMessage.value = ''
}

// Close sidebar on route change (mobile)
watch(() => useRoute().path, () => {
  sidebarOpen.value = false
})
</script>

<style scoped>
.sidebar-item {
  @apply flex items-center px-4 py-3 text-gray-300 hover:bg-yellow-400 hover:text-black transition-colors duration-200 cursor-pointer rounded-lg;
}

.sidebar-item.active {
  @apply bg-yellow-400 text-black font-semibold;
}

.chat-popup {
  @apply fixed bottom-4 right-4 w-80 h-96 bg-white rounded-lg shadow-2xl border border-gray-200 z-50 flex flex-col;
}

.chat-header {
  @apply bg-yellow-400 text-black px-4 py-3 rounded-t-lg font-semibold flex justify-between items-center;
}

.chat-messages {
  @apply flex-1 p-4 overflow-y-auto space-y-3;
}

.chat-input {
  @apply border-t border-gray-200 p-3;
}
</style>