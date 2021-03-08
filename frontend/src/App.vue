<template>
  <div id="app">
    <nav class="navbar navbar-inverse" style="background: rgba(0,0,0,0); color: #eee; font-weight: bolder;
      font-size: 120%;">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Theta TV</a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li id="home-bt" v-if="loginsess" v-bind:class="homeTabClass" v-on:click="dashboard" >
              <a href="#">BOT</a></li>
            <li id="list-bt" v-if="loginsess" v-bind:class="listTabClass" v-on:click="favoriteList"><a href="#">
              <i class="glyphicon glyphicon-list-alt"></i> MENU 2</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li id="active" v-if="loginsess"><a href="#"><span class="glyphicon glyphicon-user"></span> <span>{{activeName.charAt(0).toUpperCase() + activeName.substring(1)}}</span></a></li>
            <li v-if="loginsess" v-on:click="logout"><a href="#">Logout <span class="glyphicon glyphicon-log-out"></span></a></li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view v-if="logoutsess" @message="setSession"/>
    <Dashboard v-if="loginsess" v-bind:activeUser="activeUser" v-bind:activeName="activeName.charAt(0).toUpperCase() + activeName.substring(1)" v-bind:showList="showList" v-bind:hideList="showList" />
    <notifications group="foo" />
  </div>
</template>

<script>
import axios from 'axios'
// import Cookies from 'js-cookie'
import Dashboard from './components/Dashboard'
import Index from './components/Index'
const API_URL = 'http://128.199.12.188:8000'
export default {
  name: 'App',
  components: {Index, Dashboard},
  data () {
    return {
      message: '',
      lists: [],
      loginsess: false,
      logoutsess: true,
      activeName: '',
      activeUser: '',
      showList: true,
      // hideList: false,
      homeTabClass: 'active navz',
      listTabClass: 'navz hidden'
    }
  },
  created () {

  },
  methods: {
    setSession (act) {
      this.loginsess = act.a
      this.logoutsess = act.b
      this.activeName = act.c
      this.activeUser = act.d
    },
    logout () {
      this.loginsess = false
      this.logoutsess = true
      this.activeName = ''
      this.activeUser = ''
    },
    favoriteList () {
      if (this.loginsess) {
        this.showList = false
        // this.hideList = true
        this.listTabClass = 'active navz'
        this.homeTabClass = 'navz'
      } else {
        this.logout()
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'YOU ARE NOT LOGGED IN, KINDLY LOGIN WITH YOUR CREDENTIALS.'
        })
      }
    },
    dashboard () {
      if (this.loginsess) {
        this.showList = true
        // this.hideList = false
        this.listTabClass = 'navz'
        this.homeTabClass = 'active navz'
      } else {
        this.logout()
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'YOU ARE NOT LOGGED IN, KINDLY LOGIN WITH YOUR CREDENTIALS.'
        })
      }
    },
    // The remaining functions bellow are to test the API endpoints
    privateMessage () {
      const url = `${API_URL}/api/list/`
      // ListEnpoint [POST] (creates a new list)
      return axios.post(
        url,
        {
          email: 'koladee1@favorite.com',
          title: 'This is just a title',
          des: 'A detailed description goes here.',
          cat: 1,
          ranking: 1
        },
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage2 (who) {
      // ProfileEnpoint [GET] (fetch a single user detail)
      const url = `${API_URL}/api/profile/?who=${who}`
      return axios.get(
        url,
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage3 () {
      // ProfileEnpoint [POST] (creates a new user)
      const url = `${API_URL}/api/profile/`
      return axios.post(
        url,
        {
          email: 'koladee1@favorite.com',
          username: 'Boss',
          password: 'password',
          password2: 'password',
          fname: 'Kolade',
          lname: 'Emmanuel'
        },
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage4 () {
      // CategoryEnpoint [POST] (creates a new category)
      const url = `${API_URL}/api/category/`
      return axios.post(
        url,
        {
          email: 'koladee1@favorite.com',
          name: 'Bills'
        },
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage5 (who) {
      // CategoryEndpoint [GET] (fetches all category available for a single user)
      const url = `${API_URL}/api/category/?who=${who}`
      return axios.get(
        url,
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage6 () {
      // ListEndpoint [PUT] (updates records of a favorite list)
      const url = `${API_URL}/api/list/`
      return axios.put(
        url,
        {
          id: 7,
          email: 'koladee1@favorite.com',
          title: 'This is just a title oooo',
          des: 'A detailed description goes here.......',
          cat: 1,
          ranking: 8
        },
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.privateMessage9('koladee1@favorite.com')
      })
    },
    privateMessage7 () {
      // CategoryEndpoint [PUT] (updates records of a category)
      const url = `${API_URL}/api/category/`
      return axios.put(
        url,
        {
          id: 1,
          email: 'admin@favorite.com',
          name: 'Lagos'
        },
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage8 () {
      // ProfileEndpoint [PUT] (updates records of a profile)
      const url = `${API_URL}/api/profile/`
      return axios.put(
        url,
        {
          id: 3,
          email: 'admin@favorite.com',
          fname: 'Lagos',
          lname: 'Ikeja'
        },
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    },
    privateMessage9 (who) {
      // ListEndpoint [GET] (fetches the record of a favorite list)
      const url = `${API_URL}/api/list/?who=${who}`
      return axios.get(
        url,
        {
          headers: {}
        }).then((response) => {
        console.log(response.data)
      })
    }
  }
}
</script>
<style scoped>

</style>
