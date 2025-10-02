<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Kullanım Takibi</h1>
          <p class="text-gray-600">İnternet kullanımınızı günlük ve aylık bazda takip edin</p>
        </div>
        <div class="mt-4 md:mt-0 flex space-x-4">
          <select 
            v-model="selectedPeriod" 
            @change="fetchUsageData"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
          >
            <option value="daily">Günlük</option>
            <option value="monthly">Aylık</option>
          </select>
          <button 
            @click="fetchUsageData"
            class="bg-red-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-red-700 transition-colors"
          >
            <Icon name="heroicons:arrow-path" class="w-4 h-4 mr-2" />
            Yenile
          </button>
        </div>
      </div>
    </div>

    <!-- Current Month Summary -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">Bu Ay Toplam</p>
            <p class="text-3xl font-bold text-gray-900">{{ monthlyUsage?.total_usage_gb || 0 }} GB</p>
            <p class="text-sm text-blue-600">{{ currentPlan?.quota_gb }} GB Kotadan</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Icon name="heroicons:chart-bar" class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">Günlük Ortalama</p>
            <p class="text-3xl font-bold text-gray-900">{{ dailyAverage }} GB</p>
            <p class="text-sm text-green-600">Son 30 Gün</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <Icon name="heroicons:calendar-days" class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-yellow-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500">Kalan Kota</p>
            <p class="text-3xl font-bold text-gray-900">{{ remainingQuota }} GB</p>
            <p class="text-sm" :class="usagePercentage > 80 ? 'text-red-600' : 'text-yellow-600'">
              %{{ usagePercentage }} Kullanıldı
            </p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <Icon name="heroicons:battery-100" class="w-6 h-6 text-yellow-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Chart -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ selectedPeriod === 'daily' ? 'Günlük Kullanım Grafiği' : 'Aylık Kullanım Grafiği' }}
        </h3>
        <div class="text-sm text-gray-500">
          Son {{ selectedPeriod === 'daily' ? '30 gün' : '12 ay' }}
        </div>
      </div>
      
      <!-- Chart Container -->
      <div class="h-80 relative">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>

    <!-- Detailed Usage Table -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-6">Detaylı Kullanım Tablosu</h3>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-32">
        <Icon name="heroicons:arrow-path" class="w-8 h-8 animate-spin text-red-600" />
        <span class="ml-2 text-gray-600">Veriler yükleniyor...</span>
      </div>

      <!-- Usage Table -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ selectedPeriod === 'daily' ? 'Tarih' : 'Ay' }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Kullanım (GB)
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                İndirme (GB)
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Yükleme (GB)
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Yoğunluk
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(usage, index) in usageData" :key="index" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ formatDate(usage.date || usage.month) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ usage.used_gb || usage.total_usage_gb }} GB
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ (usage.download_gb || usage.used_gb * 0.8).toFixed(1) }} GB
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ (usage.upload_gb || usage.used_gb * 0.2).toFixed(1) }} GB
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span 
                  class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                  :class="getUsageIntensityClass(usage.used_gb || usage.total_usage_gb)"
                >
                  {{ getUsageIntensity(usage.used_gb || usage.total_usage_gb) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && (!usageData || usageData.length === 0)" class="text-center py-12">
        <Icon name="heroicons:chart-bar-square" class="mx-auto w-16 h-16 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Kullanım verisi bulunamadı</h3>
        <p class="text-gray-500">Seçilen dönem için kullanım verisi mevcut değil.</p>
      </div>
    </div>

    <!-- Usage Tips -->
    <div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl p-6">
      <div class="flex items-start">
        <Icon name="heroicons:light-bulb" class="w-6 h-6 text-blue-600 mr-3 mt-1" />
        <div>
          <h3 class="text-lg font-semibold text-blue-900 mb-2">Kullanım İpuçları</h3>
          <div class="space-y-2 text-blue-800">
            <p>• Video yayınları ve büyük dosya indirmeleri en çok veri tüketir</p>
            <p>• Wi-Fi'ye bağlı cihaz sayısını sınırlandırarak kullanımı optimize edebilirsiniz</p>
            <p>• Gece saatlerinde büyük güncellemeleri yaparak günlük kullanımı dengeleyebilirsiniz</p>
            <p>• Cotayı aştığınızda hızınız düşebilir, paket yükseltmeyi değerlendirin</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Chart, registerables } from 'chart.js'

// Chart.js'i kaydet
Chart.register(...registerables)

// Sayfa başlığı
useHead({
  title: 'Kullanım Takibi - Türkcel SmartNet'
})

// Reactive data
const selectedPeriod = ref('daily')
const usageData = ref([])
const monthlyUsage = ref(null)
const currentPlan = ref(null)
const loading = ref(true)
const chartCanvas = ref(null)
let chartInstance = null

// API config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Computed properties
const usagePercentage = computed(() => {
  if (!monthlyUsage.value || !currentPlan.value?.quota_gb) return 0
  return Math.round((monthlyUsage.value.total_usage_gb / currentPlan.value.quota_gb) * 100)
})

const remainingQuota = computed(() => {
  if (!monthlyUsage.value || !currentPlan.value?.quota_gb) return 0
  return Math.max(0, currentPlan.value.quota_gb - monthlyUsage.value.total_usage_gb)
})

const dailyAverage = computed(() => {
  if (!usageData.value.length) return 0
  const total = usageData.value.reduce((sum, usage) => sum + (usage.used_gb || usage.total_usage_gb), 0)
  return (total / usageData.value.length).toFixed(1)
})

// Methods
const fetchUsageData = async () => {
  loading.value = true
  try {
    // Kullanıcı dashboard bilgilerini çek
    const dashboardResponse = await $fetch(`${apiBase}/users/U1/dashboard`)
    currentPlan.value = dashboardResponse.current_plan
    
    // Aylık kullanım bilgilerini çek
    const monthlyResponse = await $fetch(`${apiBase}/usage/U1/monthly`)
    monthlyUsage.value = monthlyResponse
    
    // Seçilen döneme göre veri çek
    if (selectedPeriod.value === 'daily') {
      const response = await $fetch(`${apiBase}/usage/U1/daily?days=30`)
      usageData.value = response.reverse() // Tarihe göre sırala
    } else {
      // Aylık veri için mock data (API'de henüz endpoint yok)
      usageData.value = Array.from({ length: 12 }, (_, i) => ({
        month: new Date(2024, i, 1).toISOString(),
        total_usage_gb: Math.floor(Math.random() * 250) + 50
      }))
    }
    
    updateChart()
    
  } catch (error) {
    console.error('Kullanım verileri yüklenirken hata:', error)
    usageData.value = []
  } finally {
    loading.value = false
  }
}

const updateChart = () => {
  if (!chartCanvas.value) return
  
  // Önceki chart'ı temizle
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  const ctx = chartCanvas.value.getContext('2d')
  
  const labels = usageData.value.map(usage => 
    selectedPeriod.value === 'daily' 
      ? formatDate(usage.date)
      : formatMonth(usage.month)
  )
  
  const data = usageData.value.map(usage => usage.used_gb || usage.total_usage_gb)
  
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: selectedPeriod.value === 'daily' ? 'Günlük Kullanım (GB)' : 'Aylık Kullanım (GB)',
        data,
        borderColor: '#e60012',
        backgroundColor: 'rgba(230, 0, 18, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#e60012',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            callback: function(value) {
              return value + ' GB'
            }
          }
        },
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  })
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.getDate() + '/' + (date.getMonth() + 1)
}

const formatMonth = (dateString) => {
  const date = new Date(dateString)
  const months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
  return months[date.getMonth()]
}

const getUsageIntensity = (usage) => {
  if (usage < 5) return 'Düşük'
  if (usage < 15) return 'Orta'
  if (usage < 30) return 'Yüksek'
  return 'Çok Yüksek'
}

const getUsageIntensityClass = (usage) => {
  if (usage < 5) return 'bg-green-100 text-green-800'
  if (usage < 15) return 'bg-yellow-100 text-yellow-800'
  if (usage < 30) return 'bg-orange-100 text-orange-800'
  return 'bg-red-100 text-red-800'
}

// Lifecycle
onMounted(() => {
  fetchUsageData()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>