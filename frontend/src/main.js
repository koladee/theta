// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Notifications from 'vue-notification'

Vue.config.productionTip = false
Vue.use(Notifications)
Vue.component('spinner', {
  template: '<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div>' +
    '</div><div></div><div></div><div></div><div></div><div></div></div>'
})
Vue.component('roller', {
  template: '<center style="margin-top: 20%; margin-bottom: 20%;"><div class="lds-roller"><div></div><div></div><div>' +
    '</div><div></div><div></div><div></div><div></div><div></div></div></center>'
})
Vue.component('rarr', {
  template: '<span class="glyphicon glyphicon-send"></span>'
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
