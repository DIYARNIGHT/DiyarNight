<template>
  <div class="space-y-6">
    <!-- Welcome Header -->
    <div class="bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl text-white p-8">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-3xl font-bold mb-2">Hoş geldiniz, {{ userDashboard?.user?.name }}!</h1>
          <p class="text-gray-300 text-lg">
            {{ userDashboard?.current_plan?.name }} paketinizle internete hızla bağlı kalın
          </p>
        </div>
        <div class="mt-4 md:mt-0 flex space-x-4">
          <button 
            @click="runSpeedTest"
            :disabled="speedTestLoading"
            class="bg-yellow-400 text-black px-6 py-3 rounded-lg font-semibold hover:bg-yellow-500 transition-colors disabled:opacity-50"
          >
            <Icon v-if="speedTestLoading" name="heroicons:arrow-path" class="w-5 h-5 animate-spin mr-2" />
            {{ speedTestLoading ? 'Test Yapılıyor...' : 'Hız Testi' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Speed Test Results -->
    <div v-if="speedTestResult" class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
      <div class="flex items-center mb-4">
        <Icon name="heroicons:signal" class="w-6 h-6 text-green-500 mr-3" />
        <h3 class="text-lg font-semibold text-gray-900">Hız Testi Sonucu</h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center">
          <p class="text-3xl font-bold text-green-600">{{ speedTestResult.download_speed }}</p>
          <p class="text-sm text-gray-500">Mbps İndirme</p>
        </div>
        <div class="text-center">
          <p class="text-3xl font-bold text-blue-600">{{ speedTestResult.upload_speed }}</p>
          <p class="text-sm text-gray-500">Mbps Yükleme</p>
        </div>
        <div class="text-center">
          <p class="text-3xl font-bold text-purple-600">{{ speedTestResult.ping }}</p>
          <p class="text-sm text-gray-500">ms Ping</p>
        </div>
      </div>
    </div>

    <!-- Main Dashboard Grid: Sol Panel + Sağ Panel -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Sol Panel: Mevcut Paket, Kota Durumu, Hız -->
      <div class="lg:col-span-2 space-y-6">
        
        <!-- Mevcut Paket Bilgileri -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-yellow-400">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-semibold text-gray-900">Mevcut Paketiniz</h3>
            <div class="bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-semibold">
              Aktif
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="w-12 h-12 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-3">
                <Icon name="heroicons:wifi" class="w-6 h-6 text-black" />
              </div>
              <h4 class="font-semibold text-gray-900">{{ userDashboard?.current_plan?.name }}</h4>
              <p class="text-2xl font-bold text-yellow-500">{{ userDashboard?.current_plan?.speed_mbps }}</p>
              <p class="text-sm text-gray-600">Mbps Hız</p>
            </div>
            
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-3">
                <Icon name="heroicons:banknotes" class="w-6 h-6 text-yellow-400" />
              </div>
              <h4 class="font-semibold text-gray-900">Aylık Ücret</h4>
              <p class="text-2xl font-bold text-gray-800">₺{{ userDashboard?.current_plan?.monthly_price }}</p>
              <p class="text-sm text-gray-600">Sabit Fiyat</p>
            </div>
            
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="w-12 h-12 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-3">
                <Icon name="heroicons:calendar-days" class="w-6 h-6 text-black" />
              </div>
              <h4 class="font-semibold text-gray-900">Paket Başlangıç</h4>
              <p class="text-lg font-bold text-gray-800">01.10.2024</p>
              <p class="text-sm text-gray-600">Aktivasyon</p>
            </div>
          </div>
        </div>

        <!-- Kota Durumu -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-semibold text-gray-900">Kota Kullanım Durumu</h3>
            <span class="text-sm text-gray-500">{{ monthlyUsage?.total_usage_gb || 0 }} / {{ userDashboard?.current_plan?.quota_gb }} GB</span>
          </div>
          
          <!-- Progress Bar -->
          <div class="w-full bg-gray-200 rounded-full h-6 mb-4">
            <div 
              class="h-6 rounded-full transition-all duration-500 flex items-center justify-center text-white text-xs font-semibold"
              :class="usagePercentage > 80 ? 'bg-red-500' : usagePercentage > 60 ? 'bg-yellow-400 text-black' : 'bg-green-500'"
              :style="{ width: Math.min(usagePercentage, 100) + '%' }"
            >
              %{{ usagePercentage }}
            </div>
          </div>
          
          <div class="grid grid-cols-3 gap-4 text-center">
            <div>
              <p class="text-2xl font-bold text-blue-600">{{ monthlyUsage?.total_usage_gb || 0 }}</p>
              <p class="text-sm text-gray-600">Kullanılan</p>
            </div>
            <div>
              <p class="text-2xl font-bold text-green-600">{{ remainingQuota }}</p>
              <p class="text-sm text-gray-600">Kalan</p>
            </div>
            <div>
              <p class="text-2xl font-bold" :class="usagePercentage > 80 ? 'text-red-600' : usagePercentage > 60 ? 'text-yellow-600' : 'text-green-600'">
                {{ usagePercentage > 80 ? 'Kritik' : usagePercentage > 60 ? 'Dikkat' : 'Normal' }}
              </p>
              <p class="text-sm text-gray-600">Durum</p>
            </div>
          </div>
        </div>

        <!-- Hız Takibi -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-4">Hız Performansı</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <Icon name="heroicons:arrow-down" class="w-8 h-8 text-green-600 mx-auto mb-2" />
              <p class="text-lg font-bold text-gray-900">{{ lastSpeedTest?.download || '95' }}</p>
              <p class="text-xs text-gray-600">İndirme Mbps</p>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <Icon name="heroicons:arrow-up" class="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <p class="text-lg font-bold text-gray-900">{{ lastSpeedTest?.upload || '45' }}</p>
              <p class="text-xs text-gray-600">Yükleme Mbps</p>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <Icon name="heroicons:bolt" class="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <p class="text-lg font-bold text-gray-900">{{ lastSpeedTest?.ping || '12' }}</p>
              <p class="text-xs text-gray-600">Ping ms</p>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <Icon name="heroicons:signal" class="w-8 h-8 text-yellow-600 mx-auto mb-2" />
              <p class="text-lg font-bold text-gray-900">%98</p>
              <p class="text-xs text-gray-600">Uptime</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Sağ Panel: Önerilen Paket, Ek Paket, Destek Aksiyonları -->
      <div class="space-y-6">
        
        <!-- Önerilen Paket -->
        <div class="bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-xl text-black p-6">
          <div class="flex items-center mb-4">
            <Icon name="heroicons:light-bulb" class="w-6 h-6 mr-3" />
            <h3 class="text-lg font-semibold">Size Özel Öneri</h3>
          </div>
          
          <div class="space-y-4">
            <div v-if="usagePercentage > 80" class="bg-white bg-opacity-20 rounded-lg p-4">
              <h4 class="font-semibold mb-2">Kota Yükseltme</h4>
              <p class="text-sm mb-3">Kotanız %{{ usagePercentage }} doldu. Üst pakete geçerek daha rahat kullanım sağlayabilirsiniz.</p>
              <button class="w-full bg-black text-yellow-400 py-2 rounded-lg font-semibold hover:bg-gray-800 transition-colors">
                Fiber 250'ye Yükselt
              </button>
            </div>
            
            <div v-else class="bg-white bg-opacity-20 rounded-lg p-4">
              <h4 class="font-semibold mb-2">Ek Hizmetler</h4>
              <p class="text-sm mb-3">Ev WiFi güvenliği ve antivirüs paketi ile güvenliğinizi artırın.</p>
              <button class="w-full bg-black text-yellow-400 py-2 rounded-lg font-semibold hover:bg-gray-800 transition-colors">
                Güvenlik Paketi
              </button>
            </div>
          </div>
        </div>

        <!-- Ek Paket Butonları -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Ek Paketler</h3>
          <div class="space-y-3">
            <button 
              @click="addExtraQuota"
              :disabled="extraQuotaLoading"
              class="w-full bg-yellow-400 text-black py-3 px-4 rounded-lg font-semibold hover:bg-yellow-500 transition-colors disabled:opacity-50 flex items-center justify-center"
            >
              <Icon v-if="extraQuotaLoading" name="heroicons:arrow-path" class="w-4 h-4 animate-spin mr-2" />
              <Icon v-else name="heroicons:plus" class="w-4 h-4 mr-2" />
              {{ extraQuotaLoading ? 'Ekleniyor...' : '+50 GB Ek Kota' }}
            </button>
            
            <button class="w-full bg-gray-800 text-white py-3 px-4 rounded-lg font-semibold hover:bg-gray-900 transition-colors flex items-center justify-center">
              <Icon name="heroicons:tv" class="w-4 h-4 mr-2" />
              TV+ Paketi Ekle
            </button>
            
            <button class="w-full bg-gray-800 text-white py-3 px-4 rounded-lg font-semibold hover:bg-gray-900 transition-colors flex items-center justify-center">
              <Icon name="heroicons:device-phone-mobile" class="w-4 h-4 mr-2" />
              Mobil Hat Ekle
            </button>
          </div>
        </div>

        <!-- Destek Aksiyonları -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Hızlı Destek</h3>
          <div class="space-y-3">
            <button 
              @click="resetModem"
              :disabled="modemResetLoading"
              class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center"
            >
              <Icon v-if="modemResetLoading" name="heroicons:arrow-path" class="w-4 h-4 animate-spin mr-2" />
              <Icon v-else name="heroicons:arrow-path" class="w-4 h-4 mr-2" />
              {{ modemResetLoading ? 'Sıfırlanıyor...' : 'Modem Sıfırla' }}
            </button>
            
            <button 
              @click="reportIssue"
              class="w-full bg-red-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-red-700 transition-colors flex items-center justify-center"
            >
              <Icon name="heroicons:exclamation-triangle" class="w-4 h-4 mr-2" />
              Arıza Bildir
            </button>
            
            <nuxt-link 
              to="/support"
              class="w-full bg-green-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center justify-center"
            >
              <Icon name="heroicons:chat-bubble-left-right" class="w-4 h-4 mr-2" />
              Canlı Destek
            </nuxt-link>
          </div>
        </div>

        <!-- Sistem Durumu -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Sistem Durumu</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Bağlantı</span>
              <div class="flex items-center">
                <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                <span class="text-sm font-medium text-green-600">Online</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Modem</span>
              <div class="flex items-center">
                <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                <span class="text-sm font-medium text-green-600">Normal</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Altyapı</span>
              <div class="flex items-center">
                <div class="w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                <span class="text-sm font-medium text-yellow-600">Bakım</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Son Kullanım Grafiği -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-6">Son 7 Günlük Kullanım</h3>
      <div class="h-64 flex items-end justify-between space-x-2">
        <div 
          v-for="(usage, index) in recentUsage" 
          :key="index"
          class="flex-1 bg-yellow-400 rounded-t-lg hover:bg-yellow-500 transition-colors relative group"
          :style="{ height: (usage.used_gb / maxUsage * 200) + 'px' }"
        >
          <div class="absolute -top-10 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity">
            {{ usage.used_gb }}GB
          </div>
          <div class="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs text-gray-500">
            {{ formatDate(usage.date) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Sayfa başlığı
useHead({
  title: 'Dashboard - SmartNet'
})

// Reactive data
const userDashboard = ref(null)
const monthlyUsage = ref(null)
const recentUsage = ref([])
const speedTestResult = ref(null)
const lastSpeedTest = ref(null)
const speedTestLoading = ref(false)
const modemResetLoading = ref(false)
const extraQuotaLoading = ref(false)

// API config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Computed properties
const usagePercentage = computed(() => {
  if (!monthlyUsage.value || !userDashboard.value?.current_plan?.quota_gb) return 0
  return Math.round((monthlyUsage.value.total_usage_gb / userDashboard.value.current_plan.quota_gb) * 100)
})

const remainingQuota = computed(() => {
  if (!monthlyUsage.value || !userDashboard.value?.current_plan?.quota_gb) return 0
  return Math.max(0, userDashboard.value.current_plan.quota_gb - monthlyUsage.value.total_usage_gb)
})

const maxUsage = computed(() => {
  if (!recentUsage.value.length) return 1
  return Math.max(...recentUsage.value.map(u => u.used_gb))
})

// Methods
const fetchDashboardData = async () => {
  try {
    // Dashboard verilerini çek
    const dashboardResponse = await $fetch(`${apiBase}/users/U1/dashboard`)
    userDashboard.value = dashboardResponse
    
    // Aylık kullanım verilerini çek
    const monthlyResponse = await $fetch(`${apiBase}/usage/U1/monthly`)
    monthlyUsage.value = monthlyResponse
    
    // Son kullanım verilerini çek
    const usageResponse = await $fetch(`${apiBase}/usage/U1/daily?days=7`)
    recentUsage.value = usageResponse.reverse() // Tarihe göre sırala
    
  } catch (error) {
    console.error('Dashboard verileri yüklenirken hata:', error)
    // Hata durumunda varsayılan veriler
    userDashboard.value = {
      user: { name: 'Kullanıcı' },
      current_plan: { name: 'Fiber 100', speed_mbps: 100, quota_gb: 300, monthly_price: 399 }
    }
    monthlyUsage.value = { total_usage_gb: 240 }
    recentUsage.value = [
      { date: '2025-09-26', used_gb: 15 },
      { date: '2025-09-27', used_gb: 22 },
      { date: '2025-09-28', used_gb: 18 },
      { date: '2025-09-29', used_gb: 25 },
      { date: '2025-09-30', used_gb: 31 },
      { date: '2025-10-01', used_gb: 28 },
      { date: '2025-10-02', used_gb: 35 }
    ]
  }
}

const runSpeedTest = async () => {
  speedTestLoading.value = true
  try {
    const response = await $fetch(`${apiBase}/users/U1/speed-test`, {
      method: 'POST'
    })
    speedTestResult.value = response
    lastSpeedTest.value = response
  } catch (error) {
    console.error('Hız testi hatası:', error)
    // Mock data
    speedTestResult.value = {
      download_speed: '95.2',
      upload_speed: '45.8',
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
    
    alert('Modem sıfırlama komutu gönderildi! 2-3 dakika içinde modem yeniden başlayacak.')
    
  } catch (error) {
    console.error('Modem sıfırlama hatası:', error)
    alert('Modem sıfırlama işlemi başarısız oldu. Lütfen tekrar deneyin.')
  } finally {
    modemResetLoading.value = false
  }
}

const addExtraQuota = async () => {
  extraQuotaLoading.value = true
  try {
    // API call for extra quota
    await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate API call
    alert('50 GB ek kota paketinize eklendi! Bu ay için geçerlidir.')
  } catch (error) {
    alert('Ek kota ekleme işlemi başarısız oldu.')
  } finally {
    extraQuotaLoading.value = false
  }
}

const reportIssue = () => {
  navigateTo('/support?action=report')
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.getDate() + '/' + (date.getMonth() + 1)
}

// Sayfa yüklendiğinde verileri çek
onMounted(() => {
  fetchDashboardData()
})
</script>