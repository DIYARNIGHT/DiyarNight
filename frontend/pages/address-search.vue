<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Adres Sorgulama</h1>
          <p class="text-gray-600">Adresinizin altyapı durumunu ve kullanılabilir internet paketlerini öğrenin</p>
        </div>
        <div class="mt-4 md:mt-0 flex items-center space-x-3">
          <div class="bg-yellow-400 text-black px-4 py-2 rounded-lg font-semibold text-sm">
            <Icon name="heroicons:signal" class="w-4 h-4 mr-2 inline" />
            Altyapı Sorgulama
          </div>
        </div>
      </div>
    </div>

    <!-- Address Search Form -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">Adres Bilgilerinizi Girin</h2>
      
      <form @submit.prevent="searchAddress" class="space-y-6">
        <!-- City Selection -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">İl Seçin</label>
            <select 
              v-model="searchForm.city"
              @change="onCityChange"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
              required
            >
              <option value="">İl Seçin</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">İlçe Seçin</label>
            <select 
              v-model="searchForm.district"
              @change="onDistrictChange"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
              :disabled="!searchForm.city"
              required
            >
              <option value="">İlçe Seçin</option>
              <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
            </select>
          </div>
        </div>

        <!-- Neighborhood and Address -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Mahalle</label>
            <select 
              v-model="searchForm.neighborhood"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
              :disabled="!searchForm.district"
              required
            >
              <option value="">Mahalle Seçin</option>
              <option v-for="neighborhood in neighborhoods" :key="neighborhood" :value="neighborhood">{{ neighborhood }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Sokak/Cadde</label>
            <input 
              v-model="searchForm.street"
              type="text" 
              placeholder="Sokak/Cadde adını girin"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
              required
            >
          </div>
        </div>

        <!-- Building Details -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Bina No</label>
            <input 
              v-model="searchForm.buildingNumber"
              type="text" 
              placeholder="Bina numarası"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Daire No</label>
            <input 
              v-model="searchForm.apartmentNumber"
              type="text" 
              placeholder="Daire numarası"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Posta Kodu</label>
            <input 
              v-model="searchForm.postalCode"
              type="text" 
              placeholder="Posta kodu"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400"
            >
          </div>
        </div>

        <!-- Search Button -->
        <div class="flex justify-center">
          <button 
            type="submit"
            :disabled="searching"
            class="bg-yellow-400 text-black px-8 py-3 rounded-lg font-semibold hover:bg-yellow-500 transition-colors disabled:opacity-50 flex items-center"
          >
            <Icon v-if="searching" name="heroicons:arrow-path" class="w-5 h-5 animate-spin mr-2" />
            <Icon v-else name="heroicons:magnifying-glass" class="w-5 h-5 mr-2" />
            {{ searching ? 'Sorgulanıyor...' : 'Adres Sorgula' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults" class="space-y-6">
      <!-- Infrastructure Status -->
      <div class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-semibold text-gray-900">Altyapı Durumu</h3>
          <div 
            class="px-4 py-2 rounded-full text-sm font-semibold"
            :class="getInfrastructureStatusClass(searchResults.infrastructure_available)"
          >
            {{ searchResults.infrastructure_available ? 'Altyapı Mevcut' : 'Altyapı Yok' }}
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Fiber Status -->
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center"
                 :class="searchResults.fiber_available ? 'bg-green-100' : 'bg-red-100'">
              <Icon 
                name="heroicons:wifi" 
                class="w-6 h-6"
                :class="searchResults.fiber_available ? 'text-green-600' : 'text-red-600'"
              />
            </div>
            <h4 class="font-semibold text-gray-900">Fiber</h4>
            <p class="text-sm text-gray-600">{{ searchResults.fiber_available ? 'Mevcut' : 'Mevcut Değil' }}</p>
            <p v-if="searchResults.fiber_available" class="text-xs text-green-600 mt-1">
              Max {{ searchResults.max_speed_mbps }} Mbps
            </p>
          </div>

          <!-- ADSL Status -->
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center"
                 :class="searchResults.adsl_available ? 'bg-green-100' : 'bg-red-100'">
              <Icon 
                name="heroicons:signal" 
                class="w-6 h-6"
                :class="searchResults.adsl_available ? 'text-green-600' : 'text-red-600'"
              />
            </div>
            <h4 class="font-semibold text-gray-900">ADSL</h4>
            <p class="text-sm text-gray-600">{{ searchResults.adsl_available ? 'Mevcut' : 'Mevcut Değil' }}</p>
          </div>

          <!-- Installation Status -->
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center bg-blue-100">
              <Icon name="heroicons:calendar-days" class="w-6 h-6 text-blue-600" />
            </div>
            <h4 class="font-semibold text-gray-900">Kurulum</h4>
            <p class="text-sm text-gray-600">{{ searchResults.installation_time_days }} gün</p>
            <p class="text-xs text-blue-600 mt-1">Tahmini süre</p>
          </div>
        </div>
      </div>

      <!-- Available Plans -->
      <div v-if="searchResults.available_plans && searchResults.available_plans.length > 0" class="bg-white rounded-xl shadow-lg p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">Kullanılabilir Paketler</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="plan in searchResults.available_plans" 
            :key="plan.id"
            class="border border-gray-200 rounded-lg p-6 hover:border-yellow-400 hover:shadow-lg transition-all"
          >
            <div class="text-center">
              <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ plan.name }}</h4>
              <div class="text-3xl font-bold text-yellow-500 mb-1">{{ plan.speed_mbps }}</div>
              <p class="text-sm text-gray-600 mb-4">Mbps</p>
              
              <div class="space-y-2 mb-6">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Kota:</span>
                  <span class="font-medium">{{ plan.quota_gb }} GB</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Fiyat:</span>
                  <span class="font-medium">₺{{ plan.monthly_price }}/ay</span>
                </div>
              </div>
              
              <button 
                @click="selectPlan(plan)"
                class="w-full bg-yellow-400 text-black py-2 px-4 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
              >
                Paketi Seç
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- No Service Available -->
      <div v-else-if="searchResults && !searchResults.infrastructure_available" class="bg-white rounded-xl shadow-lg p-6">
        <div class="text-center py-8">
          <Icon name="heroicons:exclamation-triangle" class="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Altyapı Mevcut Değil</h3>
          <p class="text-gray-600 mb-6">Maalesef bu adres için henüz altyapımız bulunmamaktadır.</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-md mx-auto">
            <button 
              @click="requestInfrastructure"
              class="bg-yellow-400 text-black py-3 px-6 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
            >
              Altyapı Talebi
            </button>
            <button 
              @click="alternativeOptions"
              class="bg-gray-800 text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-900 transition-colors"
            >
              Alternatif Çözümler
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Address Search -->
    <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-xl p-6">
      <div class="flex items-start">
        <Icon name="heroicons:light-bulb" class="w-6 h-6 text-yellow-600 mr-3 mt-1" />
        <div>
          <h3 class="text-lg font-semibold text-yellow-900 mb-2">Hızlı İpuçları</h3>
          <div class="space-y-2 text-yellow-800 text-sm">
            <p>• TC Kimlik numaranızla mevcut adresinizi otomatik sorgulayabilirsiniz</p>
            <p>• Fiber altyapısı olmayan bölgelerde ADSL alternatifi sunuyoruz</p>
            <p>• Yeni yapılaşma alanları için altyapı talep edebilirsiniz</p>
            <p>• Kurulum süreleri mevsimsel koşullara göre değişiklik gösterebilir</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Sayfa başlığı
useHead({
  title: 'Adres Sorgulama - SmartNet'
})

// Reactive data
const searchForm = ref({
  city: '',
  district: '',
  neighborhood: '',
  street: '',
  buildingNumber: '',
  apartmentNumber: '',
  postalCode: ''
})

const searching = ref(false)
const searchResults = ref(null)

// API config
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Static data - Normalde API'den gelecek
const cities = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Konya', 'Gaziantep', 'Mersin', 'Kayseri']

const districtsByCity = {
  'İstanbul': ['Beyoğlu', 'Şişli', 'Beşiktaş', 'Kadıköy', 'Üsküdar', 'Fatih', 'Bakırköy', 'Zeytinburnu'],
  'Ankara': ['Çankaya', 'Keçiören', 'Yenimahalle', 'Mamak', 'Sincan', 'Pursaklar', 'Etimesgut'],
  'İzmir': ['Konak', 'Bornova', 'Karşıyaka', 'Çiğli', 'Gaziemir', 'Balçova', 'Narlıdere']
}

const neighborhoodsByDistrict = {
  'Beyoğlu': ['Galata', 'Taksim', 'Cihangir', 'Kasımpaşa'],
  'Şişli': ['Mecidiyeköy', 'Gayrettepe', 'Levent', 'Maslak'],
  'Çankaya': ['Kızılay', 'Çayyolu', 'Ümitköy', 'Bahçelievler']
}

// Computed properties
const districts = computed(() => {
  return searchForm.value.city ? districtsByCity[searchForm.value.city] || [] : []
})

const neighborhoods = computed(() => {
  return searchForm.value.district ? neighborhoodsByDistrict[searchForm.value.district] || [] : []
})

// Methods
const onCityChange = () => {
  searchForm.value.district = ''
  searchForm.value.neighborhood = ''
}

const onDistrictChange = () => {
  searchForm.value.neighborhood = ''
}

const searchAddress = async () => {
  searching.value = true
  try {
    // API'den address search endpoint'ini çağır
    const response = await $fetch(`${apiBase}/addresses/search`, {
      method: 'POST',
      body: searchForm.value
    })
    
    searchResults.value = response
    
  } catch (error) {
    console.error('Adres sorgulama hatası:', error)
    // Mock data for demo
    searchResults.value = {
      infrastructure_available: true,
      fiber_available: true,
      adsl_available: true,
      max_speed_mbps: 1000,
      installation_time_days: 5,
      available_plans: [
        {
          id: 'P1',
          name: 'Fiber 100',
          speed_mbps: 100,
          quota_gb: 500,
          monthly_price: 299
        },
        {
          id: 'P2',
          name: 'Fiber 250',
          speed_mbps: 250,
          quota_gb: 750,
          monthly_price: 399
        },
        {
          id: 'P3',
          name: 'Fiber 500',
          speed_mbps: 500,
          quota_gb: 1000,
          monthly_price: 599
        }
      ]
    }
  } finally {
    searching.value = false
  }
}

const getInfrastructureStatusClass = (available) => {
  return available 
    ? 'bg-green-100 text-green-800' 
    : 'bg-red-100 text-red-800'
}

const selectPlan = (plan) => {
  // Plan seçme işlemi
  alert(`${plan.name} paketi seçildi! Müşteri temsilcimiz size ulaşacak.`)
}

const requestInfrastructure = () => {
  alert('Altyapı talebiniz alındı! 48 saat içinde size dönüş yapılacak.')
}

const alternativeOptions = () => {
  navigateTo('/plans?alternative=true')
}
</script>