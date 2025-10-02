<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">İnternet Paketleri</h1>
          <p class="text-gray-600">Size en uygun internet paketini bulun ve hemen geçiş yapın</p>
        </div>
        <div class="mt-4 md:mt-0">
          <button 
            @click="getRecommendations"
            :disabled="recommendationsLoading"
            class="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            <Icon v-if="recommendationsLoading" name="heroicons:arrow-path" class="w-5 h-5 animate-spin mr-2" />
            {{ recommendationsLoading ? 'Analiz Ediliyor...' : 'Paket Önerisi Al' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Current Plan -->
    <div v-if="currentPlan" class="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl text-white p-6">
      <div class="flex items-center mb-4">
        <Icon name="heroicons:star" class="w-6 h-6 text-yellow-400 mr-3" />
        <h3 class="text-xl font-semibold">Mevcut Paketiniz</h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div>
          <p class="text-blue-200 text-sm">Paket Adı</p>
          <p class="text-2xl font-bold">{{ currentPlan.name }}</p>
        </div>
        <div>
          <p class="text-blue-200 text-sm">Hız</p>
          <p class="text-2xl font-bold">{{ currentPlan.speed_mbps }} Mbps</p>
        </div>
        <div>
          <p class="text-blue-200 text-sm">Kota</p>
          <p class="text-2xl font-bold">{{ currentPlan.quota_gb }} GB</p>
        </div>
        <div>
          <p class="text-blue-200 text-sm">Aylık Ücret</p>
          <p class="text-2xl font-bold">₺{{ currentPlan.monthly_price }}</p>
        </div>
      </div>
    </div>

    <!-- Recommendations -->
    <div v-if="recommendations.length > 0" class="space-y-6">
      <h2 class="text-2xl font-bold text-gray-900">Size Özel Paket Önerileri</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="recommendation in recommendations" 
          :key="recommendation.plan_id"
          class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500 relative"
        >
          <div class="absolute top-4 right-4">
            <span class="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full">
              Önerilen
            </span>
          </div>
          <div class="mb-4">
            <h3 class="text-xl font-bold text-gray-900 mb-2">{{ recommendation.plan_name }}</h3>
            <p class="text-gray-600 text-sm">{{ recommendation.reason }}</p>
          </div>
          <div class="space-y-3 mb-6">
            <div class="flex justify-between">
              <span class="text-gray-500">Hız:</span>
              <span class="font-semibold">{{ recommendation.speed_mbps }} Mbps</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Kota:</span>
              <span class="font-semibold">{{ recommendation.quota_gb }} GB</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Aylık Ücret:</span>
              <span class="font-semibold text-green-600">₺{{ recommendation.monthly_price }}</span>
            </div>
          </div>
          <button 
            @click="selectPlan(recommendation)"
            class="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
          >
            Bu Paketi Seç
          </button>
        </div>
      </div>
    </div>

    <!-- All Plans -->
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Tüm İnternet Paketleri</h2>
        <select 
          v-model="sortBy" 
          @change="sortPlans"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
        >
          <option value="speed">Hıza Göre Sırala</option>
          <option value="price">Fiyata Göre Sırala</option>
          <option value="quota">Kotaya Göre Sırala</option>
        </select>
      </div>

      <!-- Loading State -->
      <div v-if="plansLoading" class="flex justify-center items-center h-32">
        <Icon name="heroicons:arrow-path" class="w-8 h-8 animate-spin text-red-600" />
        <span class="ml-2 text-gray-600">Paketler yükleniyor...</span>
      </div>

      <!-- Plans Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="plan in sortedPlans" 
          :key="plan.id"
          class="bg-white rounded-xl shadow-lg p-6 relative transition-transform hover:scale-105"
          :class="plan.is_popular ? 'border-2 border-red-500' : 'border border-gray-200'"
        >
          <!-- Popular Badge -->
          <div v-if="plan.is_popular" class="absolute -top-3 left-1/2 transform -translate-x-1/2">
            <span class="bg-red-600 text-white text-xs font-semibold px-4 py-1 rounded-full">
              En Popüler
            </span>
          </div>

          <!-- Plan Header -->
          <div class="text-center mb-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ plan.name }}</h3>
            <div class="text-4xl font-bold text-red-600 mb-1">
              ₺{{ plan.monthly_price }}
              <span class="text-lg text-gray-500 font-normal">/ay</span>
            </div>
          </div>

          <!-- Plan Features -->
          <div class="space-y-4 mb-6">
            <div class="flex items-center">
              <Icon name="heroicons:signal" class="w-5 h-5 text-green-500 mr-3" />
              <span class="text-gray-700">{{ plan.speed_mbps }} Mbps Hız</span>
            </div>
            <div class="flex items-center">
              <Icon name="heroicons:cloud-arrow-down" class="w-5 h-5 text-blue-500 mr-3" />
              <span class="text-gray-700">{{ plan.quota_gb }} GB Aylık Kota</span>
            </div>
            <div class="flex items-center">
              <Icon name="heroicons:wifi" class="w-5 h-5 text-purple-500 mr-3" />
              <span class="text-gray-700">Ücretsiz Wi-Fi Modem</span>
            </div>
            <div class="flex items-center">
              <Icon name="heroicons:phone" class="w-5 h-5 text-orange-500 mr-3" />
              <span class="text-gray-700">7/24 Teknik Destek</span>
            </div>
            <div v-if="plan.features?.includes('fiber')" class="flex items-center">
              <Icon name="heroicons:bolt" class="w-5 h-5 text-yellow-500 mr-3" />
              <span class="text-gray-700">Fiber Altyapı</span>
            </div>
          </div>

          <!-- Comparison with Current -->
          <div v-if="currentPlan && plan.id !== currentPlan.id" class="mb-6 p-3 bg-gray-50 rounded-lg">
            <p class="text-sm text-gray-600 mb-2">Mevcut paketinizle karşılaştırma:</p>
            <div class="space-y-1 text-sm">
              <div class="flex justify-between">
                <span>Hız:</span>
                <span :class="plan.speed_mbps > currentPlan.speed_mbps ? 'text-green-600' : plan.speed_mbps < currentPlan.speed_mbps ? 'text-red-600' : 'text-gray-600'">
                  {{ plan.speed_mbps > currentPlan.speed_mbps ? '↗' : plan.speed_mbps < currentPlan.speed_mbps ? '↘' : '=' }}
                  {{ Math.abs(plan.speed_mbps - currentPlan.speed_mbps) }} Mbps
                </span>
              </div>
              <div class="flex justify-between">
                <span>Fiyat:</span>
                <span :class="plan.monthly_price < currentPlan.monthly_price ? 'text-green-600' : plan.monthly_price > currentPlan.monthly_price ? 'text-red-600' : 'text-gray-600'">
                  {{ plan.monthly_price < currentPlan.monthly_price ? '↘' : plan.monthly_price > currentPlan.monthly_price ? '↗' : '=' }}
                  ₺{{ Math.abs(plan.monthly_price - currentPlan.monthly_price) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Action Button -->
          <button 
            v-if="currentPlan && plan.id === currentPlan.id"
            disabled
            class="w-full bg-gray-400 text-white py-3 rounded-lg font-semibold cursor-not-allowed"
          >
            Mevcut Paketiniz
          </button>
          <button 
            v-else
            @click="selectPlan(plan)"
            class="w-full bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition-colors"
          >
            {{ currentPlan ? 'Bu Pakete Geç' : 'Bu Paketi Seç' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Package Comparison Modal -->
    <div v-if="showComparison" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-2xl font-bold text-gray-900">Paket Karşılaştırması</h3>
            <button @click="showComparison = false" class="text-gray-400 hover:text-gray-600">
              <Icon name="heroicons:x-mark" class="w-6 h-6" />
            </button>
          </div>
          
          <div v-if="selectedPlan" class="space-y-6">
            <div class="grid grid-cols-2 gap-6">
              <!-- Current Plan -->
              <div class="border rounded-lg p-4">
                <h4 class="font-semibold text-gray-900 mb-3">Mevcut Paketiniz</h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span>Paket:</span>
                    <span class="font-medium">{{ currentPlan?.name }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Hız:</span>
                    <span class="font-medium">{{ currentPlan?.speed_mbps }} Mbps</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Kota:</span>
                    <span class="font-medium">{{ currentPlan?.quota_gb }} GB</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Aylık Ücret:</span>
                    <span class="font-medium">₺{{ currentPlan?.monthly_price }}</span>
                  </div>
                </div>
              </div>

              <!-- Selected Plan -->
              <div class="border rounded-lg p-4 bg-red-50">
                <h4 class="font-semibold text-gray-900 mb-3">Yeni Paket</h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span>Paket:</span>
                    <span class="font-medium">{{ selectedPlan.name }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Hız:</span>
                    <span class="font-medium">{{ selectedPlan.speed_mbps }} Mbps</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Kota:</span>
                    <span class="font-medium">{{ selectedPlan.quota_gb }} GB</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Aylık Ücret:</span>
                    <span class="font-medium">₺{{ selectedPlan.monthly_price }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Confirmation -->
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div class="flex items-start">
                <Icon name="heroicons:exclamation-triangle" class="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
                <div class="text-sm text-yellow-800">
                  <p class="font-medium">Paket değişikliği hakkında:</p>
                  <ul class="mt-2 space-y-1 list-disc list-inside">
                    <li>Paket değişikliği bir sonraki fatura döneminde geçerli olur</li>
                    <li>Mevcut kotanız sıfırlanmaz, yeni döneme taşınır</li>
                    <li>İptal etmek isterseniz 14 gün içinde geri alabilirsiniz</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex space-x-4">
              <button 
                @click="showComparison = false"
                class="flex-1 bg-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
              >
                İptal Et
              </button>
              <button 
                @click="confirmPlanChange"
                class="flex-1 bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition-colors"
              >
                Paketi Değiştir
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Sayfa başlığı
useHead({
  title: 'İnternet Paketleri - Türkcel SmartNet'
})

// Reactive data
const plans = ref([])
const recommendations = ref([])
const currentPlan = ref(null)
const selectedPlan = ref(null)
const showComparison = ref(false)
const plansLoading = ref(true)
const recommendationsLoading = ref(false)
const sortBy = ref('speed')

// API config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Computed
const sortedPlans = computed(() => {
  if (!plans.value.length) return []
  
  const sorted = [...plans.value].sort((a, b) => {
    switch (sortBy.value) {
      case 'price':
        return a.monthly_price - b.monthly_price
      case 'quota':
        return b.quota_gb - a.quota_gb
      case 'speed':
      default:
        return b.speed_mbps - a.speed_mbps
    }
  })
  
  return sorted
})

// Methods
const fetchPlans = async () => {
  plansLoading.value = true
  try {
    // Tüm paketleri çek
    const plansResponse = await $fetch(`${apiBase}/plans`)
    plans.value = plansResponse
    
    // Kullanıcı dashboard bilgilerini çek
    const dashboardResponse = await $fetch(`${apiBase}/users/U1/dashboard`)
    currentPlan.value = dashboardResponse.current_plan
    
  } catch (error) {
    console.error('Paketler yüklenirken hata:', error)
    // Varsayılan paketler
    plans.value = [
      {
        id: 'P1',
        name: 'Fiber 25',
        speed_mbps: 25,
        quota_gb: 100,
        monthly_price: 199,
        is_popular: false
      },
      {
        id: 'P2',
        name: 'Fiber 50',
        speed_mbps: 50,
        quota_gb: 200,
        monthly_price: 299,
        is_popular: true
      },
      {
        id: 'P3',
        name: 'Fiber 100',
        speed_mbps: 100,
        quota_gb: 300,
        monthly_price: 399,
        is_popular: false
      }
    ]
  } finally {
    plansLoading.value = false
  }
}

const getRecommendations = async () => {
  recommendationsLoading.value = true
  try {
    const response = await $fetch(`${apiBase}/plans/recommendations/U1`)
    recommendations.value = response
  } catch (error) {
    console.error('Öneriler yüklenirken hata:', error)
    recommendations.value = []
  } finally {
    recommendationsLoading.value = false
  }
}

const selectPlan = (plan) => {
  selectedPlan.value = plan
  showComparison.value = true
}

const confirmPlanChange = async () => {
  try {
    // Plan değişikliği API'si (henüz mevcut değil, simüle edildi)
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Başarı bildirimi
    alert(`Paket değişikliği başarıyla gerçekleştirildi! ${selectedPlan.value.name} paketine geçiş talebiniz alındı.`)
    
    // Modal'ı kapat
    showComparison.value = false
    selectedPlan.value = null
    
    // Sayfayı yenile
    await fetchPlans()
    
  } catch (error) {
    console.error('Paket değişikliği hatası:', error)
    alert('Paket değişikliği sırasında bir hata oluştu. Lütfen tekrar deneyin.')
  }
}

const sortPlans = () => {
  // Computed property otomatik olarak güncellenecek
}

// Lifecycle
onMounted(() => {
  fetchPlans()
})
</script>