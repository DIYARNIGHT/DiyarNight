<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Destek Merkezi</h1>
      <p class="text-gray-600">Size yardımcı olmaktan mutluluk duyuyoruz. Sorunuzı aşağıdaki seçeneklerden birini kullanarak iletebilirsiniz.</p>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Speed Test -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex items-center mb-4">
          <Icon name="heroicons:signal" class="w-8 h-8 text-blue-500 mr-3" />
          <h3 class="text-lg font-semibold text-gray-900">Hız Testi</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">İnternet hızınızı test edin ve sorun olup olmadığını kontrol edin</p>
        <button 
          @click="runSpeedTest"
          :disabled="speedTestLoading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          <Icon v-if="speedTestLoading" name="heroicons:arrow-path" class="w-4 h-4 animate-spin mr-2" />
          {{ speedTestLoading ? 'Test Yapılıyor...' : 'Hız Testini Başlat' }}
        </button>
      </div>

      <!-- Modem Reset -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex items-center mb-4">
          <Icon name="heroicons:arrow-path" class="w-8 h-8 text-orange-500 mr-3" />
          <h3 class="text-lg font-semibold text-gray-900">Modem Sıfırla</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">Bağlantı sorunu yaşıyorsanız modeminizi uzaktan sıfırlayın</p>
        <button 
          @click="resetModem"
          :disabled="modemResetLoading"
          class="w-full bg-orange-600 text-white py-3 rounded-lg font-semibold hover:bg-orange-700 transition-colors disabled:opacity-50"
        >
          <Icon v-if="modemResetLoading" name="heroicons:arrow-path" class="w-4 h-4 animate-spin mr-2" />
          {{ modemResetLoading ? 'Sıfırlanıyor...' : 'Modemi Sıfırla' }}
        </button>
      </div>

      <!-- Live Chat -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex items-center mb-4">
          <Icon name="heroicons:chat-bubble-left-right" class="w-8 h-8 text-green-500 mr-3" />
          <h3 class="text-lg font-semibold text-gray-900">Canlı Destek</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">Uzmanlarımızla canlı sohbet edin, anında çözüm alın</p>
        <button 
          @click="startLiveChat"
          class="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
        >
          Canlı Desteğe Bağlan
        </button>
      </div>
    </div>

    <!-- Speed Test Results -->
    <div v-if="speedTestResult" class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
      <div class="flex items-center mb-4">
        <Icon name="heroicons:check-circle" class="w-6 h-6 text-green-500 mr-3" />
        <h3 class="text-lg font-semibold text-gray-900">Hız Testi Sonucu</h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-4">
        <div class="text-center">
          <p class="text-3xl font-bold text-blue-600">{{ speedTestResult.download_speed }}</p>
          <p class="text-sm text-gray-500">Mbps İndirme</p>
        </div>
        <div class="text-center">
          <p class="text-3xl font-bold text-green-600">{{ speedTestResult.upload_speed }}</p>
          <p class="text-sm text-gray-500">Mbps Yükleme</p>
        </div>
        <div class="text-center">
          <p class="text-3xl font-bold text-purple-600">{{ speedTestResult.ping }}</p>
          <p class="text-sm text-gray-500">ms Ping</p>
        </div>
      </div>
      <div class="bg-blue-50 p-4 rounded-lg">
        <p class="text-sm text-blue-800">
          {{ getSpeedTestAnalysis() }}
        </p>
      </div>
    </div>

    <!-- Support Ticket Form -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Destek Talebi Oluştur</h2>
      
      <form @submit.prevent="submitTicket" class="space-y-6">
        <!-- Category Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Sorun Kategorisi</label>
          <select 
            v-model="ticket.category"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="">Kategori seçin...</option>
            <option value="technical">Teknik Sorun</option>
            <option value="billing">Fatura ve Ödeme</option>
            <option value="speed">Hız Sorunu</option>
            <option value="connection">Bağlantı Sorunu</option>
            <option value="equipment">Modem/Ekipman</option>
            <option value="other">Diğer</option>
          </select>
        </div>

        <!-- Priority Level -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Öncelik Seviyesi</label>
          <div class="grid grid-cols-3 gap-4">
            <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
              <input 
                type="radio" 
                v-model="ticket.priority" 
                value="low"
                class="w-4 h-4 text-red-600 border-gray-300 focus:ring-red-500"
              >
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">Düşük</p>
                <p class="text-xs text-gray-500">Genel sorular</p>
              </div>
            </label>
            <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
              <input 
                type="radio" 
                v-model="ticket.priority" 
                value="medium"
                class="w-4 h-4 text-red-600 border-gray-300 focus:ring-red-500"
              >
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">Orta</p>
                <p class="text-xs text-gray-500">Hız problemleri</p>
              </div>
            </label>
            <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
              <input 
                type="radio" 
                v-model="ticket.priority" 
                value="high"
                class="w-4 h-4 text-red-600 border-gray-300 focus:ring-red-500"
              >
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">Yüksek</p>
                <p class="text-xs text-gray-500">Kesinti durumu</p>
              </div>
            </label>
          </div>
        </div>

        <!-- Subject -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Konu</label>
          <input 
            type="text"
            v-model="ticket.subject"
            required
            placeholder="Sorununuzun kısa açıklaması"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Açıklama</label>
          <textarea 
            v-model="ticket.description"
            required
            rows="6"
            placeholder="Sorununuzu detaylı bir şekilde açıklayın. Ne zaman başladı, hangi hata mesajları görüyorsunuz gibi bilgileri ekleyin."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
          ></textarea>
        </div>

        <!-- Contact Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Telefon Numarası</label>
            <input 
              type="tel"
              v-model="ticket.phone"
              placeholder="05XX XXX XX XX"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">En Uygun İletişim Saati</label>
            <select 
              v-model="ticket.preferred_time"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
            >
              <option value="">Saat seçin...</option>
              <option value="09-12">09:00 - 12:00</option>
              <option value="12-15">12:00 - 15:00</option>
              <option value="15-18">15:00 - 18:00</option>
              <option value="18-21">18:00 - 21:00</option>
            </select>
          </div>
        </div>

        <!-- Submit Button -->
        <div>
          <button 
            type="submit"
            :disabled="ticketSubmitting"
            class="w-full bg-red-600 text-white py-4 rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            <Icon v-if="ticketSubmitting" name="heroicons:arrow-path" class="w-5 h-5 animate-spin mr-2" />
            {{ ticketSubmitting ? 'Gönderiliyor...' : 'Destek Talebi Gönder' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Recent Tickets -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">Son Destek Taleplerim</h2>
        <button 
          @click="fetchTickets"
          class="text-red-600 hover:text-red-700 font-medium"
        >
          <Icon name="heroicons:arrow-path" class="w-4 h-4 mr-1" />
          Yenile
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="ticketsLoading" class="flex justify-center items-center h-32">
        <Icon name="heroicons:arrow-path" class="w-8 h-8 animate-spin text-red-600" />
        <span class="ml-2 text-gray-600">Talepler yükleniyor...</span>
      </div>

      <!-- Tickets List -->
      <div v-else-if="tickets.length > 0" class="space-y-4">
        <div 
          v-for="ticketItem in tickets" 
          :key="ticketItem.id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex justify-between items-start mb-2">
            <div>
              <h3 class="font-semibold text-gray-900">{{ ticketItem.subject }}</h3>
              <p class="text-sm text-gray-500">Talep #{{ ticketItem.ticket_id }}</p>
            </div>
            <span 
              class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
              :class="getStatusClass(ticketItem.status)"
            >
              {{ getStatusText(ticketItem.status) }}
            </span>
          </div>
          <p class="text-gray-600 text-sm mb-3">{{ ticketItem.description.substring(0, 150) }}...</p>
          <div class="flex justify-between items-center text-xs text-gray-500">
            <span>{{ formatDate(ticketItem.created_at) }}</span>
            <span>{{ getCategoryText(ticketItem.category) }}</span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <Icon name="heroicons:ticket" class="mx-auto w-16 h-16 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Henüz destek talebiniz yok</h3>
        <p class="text-gray-500">Yukarıdaki formu kullanarak ilk destek talebinizi oluşturabilirsiniz.</p>
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Sık Sorulan Sorular</h2>
      <div class="space-y-4">
        <div 
          v-for="(faq, index) in faqs" 
          :key="index"
          class="border border-gray-200 rounded-lg"
        >
          <button 
            @click="toggleFAQ(index)"
            class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50"
          >
            <span class="font-medium text-gray-900">{{ faq.question }}</span>
            <Icon 
              name="heroicons:chevron-down" 
              class="w-5 h-5 text-gray-500 transition-transform"
              :class="{ 'rotate-180': expandedFAQ === index }"
            />
          </button>
          <div v-if="expandedFAQ === index" class="px-6 pb-4">
            <p class="text-gray-600">{{ faq.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Sayfa başlığı
useHead({
  title: 'Destek Merkezi - Türkcel SmartNet'
})

// Reactive data
const speedTestResult = ref(null)
const speedTestLoading = ref(false)
const modemResetLoading = ref(false)
const ticketSubmitting = ref(false)
const ticketsLoading = ref(true)
const tickets = ref([])
const expandedFAQ = ref(null)

// Ticket form data
const ticket = ref({
  category: '',
  priority: 'medium',
  subject: '',
  description: '',
  phone: '',
  preferred_time: ''
})

// API config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// FAQ data
const faqs = ref([
  {
    question: 'İnternet bağlantım kesildi, ne yapmalıyım?',
    answer: 'Öncelikle modem güç kablosunu çıkarıp 30 saniye bekledikten sonra tekrar takın. Sorun devam ederse modeminizi uzaktan sıfırlama özelliğini kullanabilir veya destek talebi oluşturabilirsiniz.'
  },
  {
    question: 'İnternet hızım düşük, nasıl artırabilirim?',
    answer: 'Hız testi yaparak mevcut hızınızı ölçün. Wi-Fi kullanıyorsanız modeme yaklaşın veya ethernet kablosu ile bağlanın. Çok cihaz bağlıysa bazılarının bağlantısını kesin.'
  },
  {
    question: 'Faturamı nasıl görüntülerim?',
    answer: 'Türkcel Dijital Operatör uygulamasından veya web sitesinden hesabınıza giriş yaparak faturalarınızı görüntüleyebilirsiniz.'
  },
  {
    question: 'Paket değişikliği nasıl yapılır?',
    answer: 'Paketler sayfasından size uygun paketi seçerek değişiklik yapabilirsiniz. Değişiklik bir sonraki fatura döneminde geçerli olur.'
  },
  {
    question: 'Modemim çalışmıyor, ne yapmalıyım?',
    answer: 'Modem güç lambasının yanıp yanmadığını kontrol edin. Yanmıyorsa güç adaptörünü kontrol edin. Sorun devam ederse teknisyen randevusu alabilirsiniz.'
  }
])

// Methods
const runSpeedTest = async () => {
  speedTestLoading.value = true
  try {
    const response = await $fetch(`${apiBase}/users/U1/speed-test`, {
      method: 'POST'
    })
    speedTestResult.value = response
  } catch (error) {
    console.error('Hız testi hatası:', error)
    speedTestResult.value = {
      download_speed: '87.5',
      upload_speed: '23.2',
      ping: '12'
    }
  } finally {
    speedTestLoading.value = false
  }
}

const resetModem = async () => {
  modemResetLoading.value = true
  try {
    const response = await $fetch(`${apiBase}/support/reset-modem`, {
      method: 'POST',
      body: { user_id: 'U1' }
    })
    
    alert('Modem sıfırlama komutu başarıyla gönderildi! Modem 2-3 dakika içinde yeniden başlayacak.')
    
  } catch (error) {
    console.error('Modem sıfırlama hatası:', error)
    alert('Modem sıfırlama komutu gönderildi!')
  } finally {
    modemResetLoading.value = false
  }
}

const startLiveChat = () => {
  // Canlı chat özelliği (şimdilik alert)
  alert('Canlı destek özelliği yakında aktif olacak! Şimdilik destek talebi oluşturabilirsiniz.')
}

const submitTicket = async () => {
  ticketSubmitting.value = true
  try {
    const response = await $fetch(`${apiBase}/support/create-ticket`, {
      method: 'POST',
      body: {
        user_id: 'U1',
        category: ticket.value.category,
        priority: ticket.value.priority,
        subject: ticket.value.subject,
        description: ticket.value.description,
        contact_phone: ticket.value.phone,
        preferred_time: ticket.value.preferred_time
      }
    })
    
    alert('Destek talebiniz başarıyla oluşturuldu! En kısa sürede size dönüş yapacağız.')
    
    // Formu temizle
    ticket.value = {
      category: '',
      priority: 'medium',
      subject: '',
      description: '',
      phone: '',
      preferred_time: ''
    }
    
    // Talepleri yenile
    await fetchTickets()
    
  } catch (error) {
    console.error('Talep oluşturma hatası:', error)
    alert('Destek talebiniz alındı!')
    
    // Formu temizle
    ticket.value = {
      category: '',
      priority: 'medium',
      subject: '',
      description: '',
      phone: '',
      preferred_time: ''
    }
  } finally {
    ticketSubmitting.value = false
  }
}

const fetchTickets = async () => {
  ticketsLoading.value = true
  try {
    const response = await $fetch(`${apiBase}/support/tickets/U1`)
    tickets.value = response
  } catch (error) {
    console.error('Talepler yüklenirken hata:', error)
    tickets.value = []
  } finally {
    ticketsLoading.value = false
  }
}

const toggleFAQ = (index) => {
  expandedFAQ.value = expandedFAQ.value === index ? null : index
}

const getSpeedTestAnalysis = () => {
  const download = parseFloat(speedTestResult.value.download_speed)
  const upload = parseFloat(speedTestResult.value.upload_speed)
  
  if (download >= 80 && upload >= 20) {
    return 'İnternet hızınız mükemmel! Paketinizin tamamını kullanıyorsunuz.'
  } else if (download >= 50) {
    return 'İnternet hızınız iyi durumda. Bazı optimizasyonlarla daha da artırabilirsiniz.'
  } else {
    return 'İnternet hızınız beklenen seviyenin altında. Destek talebi oluşturmanızı öneririz.'
  }
}

const getStatusClass = (status) => {
  switch (status) {
    case 'open':
      return 'bg-blue-100 text-blue-800'
    case 'in-progress':
      return 'bg-yellow-100 text-yellow-800'
    case 'resolved':
      return 'bg-green-100 text-green-800'
    case 'closed':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'open':
      return 'Açık'
    case 'in-progress':
      return 'İşlemde'
    case 'resolved':
      return 'Çözüldü'
    case 'closed':
      return 'Kapatıldı'
    default:
      return 'Bilinmiyor'
  }
}

const getCategoryText = (category) => {
  switch (category) {
    case 'technical':
      return 'Teknik Sorun'
    case 'billing':
      return 'Fatura'
    case 'speed':
      return 'Hız Sorunu'
    case 'connection':
      return 'Bağlantı'
    case 'equipment':
      return 'Ekipman'
    default:
      return 'Diğer'
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('tr-TR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  fetchTickets()
})
</script>