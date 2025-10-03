<template>
  <div class="bg-gradient-to-br from-gray-900 via-gray-800 to-black">
    <div class="min-h-screen flex items-center justify-center p-4">
      <div class="max-w-md w-full">
        <!-- Logo & Brand -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-yellow-400 rounded-full mb-4">
            <svg class="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-white mb-2">SmartNet</h1>
          <p class="text-gray-400">Akıllı İnternet Yönetim Sistemi</p>
        </div>

        <!-- Login/Register Card -->
        <div class="bg-white rounded-2xl shadow-2xl p-8">
          <!-- Tabs -->
          <div class="flex mb-6 bg-gray-100 rounded-lg p-1">
            <button 
              @click="activeTab = 'login'"
              :class="activeTab === 'login' ? 'bg-yellow-400 text-black' : 'text-gray-600 hover:text-gray-900'"
              class="flex-1 py-2 rounded-lg font-semibold transition-all"
            >
              Giriş Yap
            </button>
            <button 
              @click="activeTab = 'register'"
              :class="activeTab === 'register' ? 'bg-yellow-400 text-black' : 'text-gray-600 hover:text-gray-900'"
              class="flex-1 py-2 rounded-lg font-semibold transition-all"
            >
              Kayıt Ol
            </button>
          </div>

          <!-- Login Form -->
          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Kullanıcı Adı
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <input 
                  type="text" 
                  v-model="loginForm.username"
                  required
                  placeholder="demo veya admin"
                  class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none"
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Şifre
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                </div>
                <input 
                  :type="showLoginPassword ? 'text' : 'password'"
                  v-model="loginForm.password"
                  required
                  placeholder="demo123 veya admin123"
                  class="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none"
                >
                <button 
                  type="button"
                  @click="showLoginPassword = !showLoginPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  <svg class="w-5 h-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex items-center justify-between">
              <label class="flex items-center">
                <input type="checkbox" v-model="loginForm.rememberMe" class="w-4 h-4 text-yellow-400 border-gray-300 rounded focus:ring-yellow-400">
                <span class="ml-2 text-sm text-gray-600">Beni Hatırla</span>
              </label>
              <a href="#" class="text-sm text-yellow-600 hover:text-yellow-700 font-medium">
                Şifremi Unuttum?
              </a>
            </div>

            <!-- Error Message -->
            <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center">
              <svg class="w-5 h-5 text-red-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-sm text-red-700">{{ loginError }}</p>
            </div>

            <button 
              type="submit"
              :disabled="loginLoading"
              class="w-full bg-yellow-400 text-black font-bold py-3 rounded-lg hover:bg-yellow-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              <span>{{ loginLoading ? 'Giriş Yapılıyor...' : 'Giriş Yap' }}</span>
              <svg v-if="loginLoading" class="w-5 h-5 ml-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>

            <!-- Demo Info -->
            <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p class="text-xs text-blue-800 font-semibold mb-2">🎯 Demo Hesaplar:</p>
              <div class="text-xs text-blue-700 space-y-1">
                <p><strong>Kullanıcı:</strong> demo / demo123</p>
                <p><strong>Admin:</strong> admin / admin123</p>
              </div>
            </div>
          </form>

          <!-- Register Form -->
          <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Ad Soyad
              </label>
              <input 
                type="text" 
                v-model="registerForm.name"
                required
                placeholder="Ahmet Yılmaz"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Kullanıcı Adı
              </label>
              <input 
                type="text" 
                v-model="registerForm.username"
                required
                placeholder="ahmetyilmaz"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                E-posta
              </label>
              <input 
                type="email" 
                v-model="registerForm.email"
                required
                placeholder="ahmet@example.com"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Telefon (Opsiyonel)
              </label>
              <input 
                type="tel" 
                v-model="registerForm.phone"
                placeholder="5XX XXX XX XX"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Şifre
              </label>
              <div class="relative">
                <input 
                  :type="showRegisterPassword ? 'text' : 'password'"
                  v-model="registerForm.password"
                  required
                  placeholder="En az 6 karakter"
                  minlength="6"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 outline-none pr-12"
                >
                <button 
                  type="button"
                  @click="showRegisterPassword = !showRegisterPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  <svg class="w-5 h-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                </button>
              </div>
            </div>

            <label class="flex items-start">
              <input type="checkbox" v-model="registerForm.acceptTerms" required class="w-4 h-4 text-yellow-400 border-gray-300 rounded focus:ring-yellow-400 mt-1">
              <span class="ml-2 text-sm text-gray-600">
                <a href="#" class="text-yellow-600 hover:text-yellow-700 font-medium">Kullanım Koşulları</a>nı 
                ve <a href="#" class="text-yellow-600 hover:text-yellow-700 font-medium">Gizlilik Politikası</a>nı kabul ediyorum.
              </span>
            </label>

            <!-- Error Message -->
            <div v-if="registerError" class="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center">
              <svg class="w-5 h-5 text-red-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-sm text-red-700">{{ registerError }}</p>
            </div>

            <!-- Success Message -->
            <div v-if="registerSuccess" class="bg-green-50 border border-green-200 rounded-lg p-3 flex items-center">
              <svg class="w-5 h-5 text-green-600 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-sm text-green-700">{{ registerSuccess }}</p>
            </div>

            <button 
              type="submit"
              :disabled="registerLoading"
              class="w-full bg-yellow-400 text-black font-bold py-3 rounded-lg hover:bg-yellow-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              <span>{{ registerLoading ? 'Kayıt Yapılıyor...' : 'Kayıt Ol' }}</span>
              <svg v-if="registerLoading" class="w-5 h-5 ml-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
          </form>
        </div>

        <!-- Footer -->
        <p class="text-center text-gray-400 text-sm mt-6">
          © 2025 SmartNet. Tüm hakları saklıdır.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  layout: false, // Login sayfası layout kullanmasın
  
  data() {
    return {
      activeTab: 'login',
      showLoginPassword: false,
      showRegisterPassword: false,
      
      // Login form
      loginForm: {
        username: '',
        password: '',
        rememberMe: false
      },
      loginLoading: false,
      loginError: '',
      
      // Register form
      registerForm: {
        name: '',
        username: '',
        email: '',
        phone: '',
        password: '',
        acceptTerms: false
      },
      registerLoading: false,
      registerError: '',
      registerSuccess: ''
    }
  },
  
  mounted() {
    // Eğer zaten giriş yapmışsa dashboard'a yönlendir
    this.checkExistingAuth();
  },
  
  methods: {
    checkExistingAuth() {
      const token = localStorage.getItem('auth_token');
      if (token) {
        window.location.href = '/';
      }
    },
    
    async handleLogin() {
      this.loginLoading = true;
      this.loginError = '';
      
      try {
        const response = await fetch('http://localhost:8000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.loginForm.username,
            password: this.loginForm.password
          })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
          // Save token and user info
          localStorage.setItem('auth_token', data.token);
          localStorage.setItem('user', JSON.stringify(data.user));
          
          // Redirect to dashboard and reload page
          window.location.href = '/';
          
        } else {
          this.loginError = data.detail || 'Giriş yapılırken bir hata oluştu';
        }
      } catch (error) {
        console.error('Login error:', error);
        this.loginError = 'Sunucuya bağlanılamadı. Lütfen backend\'in çalıştığından emin olun.';
      } finally {
        this.loginLoading = false;
      }
    },
    
    async handleRegister() {
      this.registerLoading = true;
      this.registerError = '';
      this.registerSuccess = '';
      
      try {
        const response = await fetch('http://localhost:8000/api/v1/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.registerForm.name,
            username: this.registerForm.username,
            email: this.registerForm.email,
            phone: this.registerForm.phone,
            password: this.registerForm.password
          })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
          this.registerSuccess = data.message || 'Kayıt başarılı! Giriş sekmesine geçiliyor...';
          
          // Reset form
          this.registerForm = {
            name: '',
            username: '',
            email: '',
            phone: '',
            password: '',
            acceptTerms: false
          };
          
          // Switch to login tab after 2 seconds
          setTimeout(() => {
            this.activeTab = 'login';
            this.loginForm.username = this.registerForm.username;
            this.registerSuccess = '';
          }, 2000);
          
        } else {
          this.registerError = data.detail || 'Kayıt olurken bir hata oluştu';
        }
      } catch (error) {
        console.error('Register error:', error);
        this.registerError = 'Sunucuya bağlanılamadı. Lütfen backend\'in çalıştığından emin olun.';
      } finally {
        this.registerLoading = false;
      }
    }
  }
}
</script>

<style scoped>
/* Custom styles for login page */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>