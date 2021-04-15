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
          <a class="navbar-brand" href="#">MrNFTBot</a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li id="home-bt" v-if="loginsess" v-bind:class="homeTabClass" v-on:click="dashboard" >
              <a href="#"><i class="glyphicon glyphicon-equalizer"></i> BOT</a></li>
            <li id="list-bt" v-if="loginsess" v-bind:class="listTabClass" v-on:click="settings">
              <a href="#"><i class="glyphicon glyphicon-cog"></i> SETTINGS</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li id="active" v-if="loginsess"><a href="#"><span class="glyphicon glyphicon-user"></span> <span>{{activeName.charAt(0).toUpperCase() + activeName.substring(1)}}</span></a></li>
            <li v-if="loginsess" v-on:click="logout"><a href="#">Logout <span class="glyphicon glyphicon-log-out"></span></a></li>
            <li v-if="!loginsess"><a href="https://www.theta.tv/account/grant-app?client_id=gxauus7bts9229e1caa7pc1rcdsiv9fq&redirect_uri=https://mrnft.gg/"><span class="glyphicon glyphicon-log-in"></span> Sign In</a></li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view v-if="logoutsess" @message="setSession"/>
    <Dashboard v-if="loginsess" v-bind:uid="uid" v-bind:activeUser="activeUser" v-bind:activeName="activeName.charAt(0).toUpperCase() + activeName.substring(1)" v-bind:showSettings="showSettings" v-bind:hideSettings="hideSettings" />
    <div v-if="!loginsess && !emotesView && showRoller">
      <div class="row" style="margin: 0px;">
        <div class="col-md-3"></div>
        <div class="col-md-6" style="padding-top: 10%;">
          <center>
            <roller></roller>
          </center>
        </div>
        <div class="col-md-3"></div>
      </div>
    </div>
    <div v-if="!loginsess && emotesView">
      <div class="row" style="padding-top: 10%; margin: 0px;">
        <div class="col-md-3"></div>
        <div class="col-md-6">
          <div class="card">
            <table v-if="JSON.stringify(emote) !== JSON.stringify({})">
              <tr>
                <td style="width: 30%;">
                  <!--forge_items id (emote id)-->
                  <!--forge_items metadata image_urls large (image src)-->
                  <!--forge_items metadata name (emote name)-->
                  <!--forge_items metadata code ":SubwaySubshappytoast:"-->
                  <div style="padding: 20px; text-align: center;">
                    <img style="height: 100px; width: 100px; border-radius: 10px 0px 10px 0px;" :src="emote.metadata.image_urls.large" alt=" "/>
                    <br>
                    <span style="font-weight: bolder; color: #ffffff; font-size: 100%;">{{emote.metadata.name}}</span>
                    <br>
                    <span class="label label-info" style="font-weight: bold; background: #ffffff; color: green; font-size: 80%;">{{emote.metadata.code}}</span>
                  </div>
                </td>
                <td style="width: 70%;">
                  <center>
                    <h2 style="color: #ffffff;">@{{activeReward.username}}</h2>
                    <span style="color: green; font-weight: bold;">LEVEL: {{activeReward.level}}</span>
                  </center>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <div class="col-md-3"></div>
      </div>
    </div>
    <notifications group="foo" />
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import Dashboard from './components/Dashboard'
import Index from './components/Index'
const API_URL = 'https://mrnft.gg'
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
      uid: '',
      showSettings: true,
      hideSettings: false,
      homeTabClass: 'active navz',
      listTabClass: 'navz',
      emotesView: false,
      activeReward: {},
      emote: {},
      emotes: [
        {
          id: 'tmp0000000000000045',
          metadata: {
            name: 'Happy Toast',
            image_urls: {
              large: 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r57wnq/avatar/emotes/4cfdf973-96a4-4bf9-988a-c24e8fad0cff.png'
            },
            code: ':SubwaySubshappytoast:'
          }
        },
        {
          id: 'tmp0000000000000122',
          metadata: {
            name: 'classyozlove',
            image_urls: {
              large: 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r57wnq/avatar/emotes/bd73434f-24a9-4a23-bc08-71b1796f01d3.png'
            },
            code: ':SubwaySubsozlove:'
          }
        },
        {
          id: 'tmp0000000000000046',
          metadata: {
            name: 'Heart Eyes Toast',
            image_urls: {
              large: 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r57wnq/avatar/emotes/9fafa613-2db4-4204-97cc-706d5c4df4c5.png'
            },
            code: ':SubwaySubshearteyes:'
          }
        },
        {
          id: 'tmp0000000000000047',
          metadata: {
            name: 'Heart',
            image_urls: {
              large: 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r57wnq/avatar/emotes/cd705520-71ca-4a22-b705-a5d3a6565f21.png'
            },
            code: ':SubwaySubsheart:'
          }
        }
      ],
      showRoller: false
    }
  },
  created () {
    if (typeof this.$route.query.code !== 'undefined') {
      if (this.$route.query.code !== '') {
        setTimeout(() => {
          this.auth()
        }, 2000)
      }
    }
    if (typeof this.$route.query.ref !== 'undefined') {
      if (this.$route.query.ref !== '') {
        setTimeout(() => {
          this.showReward('usr' + this.$route.query.ref)
        }, 2000)
      }
    }
  },
  methods: {
    showReward (a) {
      const url = `${API_URL}/api/show/reward/`
      return axios.post(
        url,
        {
          user_id: a
        },
        {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        }).then((response) => {
        // console.log(response.data)
        if (response.data.done) {
          if (response.data.data.length > 0) {
            this.activeReward = response.data.data[0]
            this.fetchGifts(a, response.data.data[0].reward)
          }
        }
      })
    },
    fetchGifts (a, b) {
      const url = `${API_URL}/api/giftable/get/`
      return axios.post(
        url,
        {
          user_id: a
        },
        {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        }).then((response) => {
        console.log(response.data)
        if (response.data.done) {
          if (response.data.data.length > 0) {
            this.emotes = response.data.data
          }
          setTimeout(() => {
            var e = 0
            for (e in this.emotes) {
              if (this.emotes[e].id === b) {
                this.emote = this.emotes[e]
                break
              }
            }
            this.loginsess = false
            this.emotesView = true
          }, 1000)
        }
      })
    },
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
    settings () {
      if (this.loginsess) {
        this.showSettings = false
        this.hideSettings = true
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
        this.showSettings = true
        this.hideSettings = false
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
    auth () {
      this.showRoller = true
      const url = `${API_URL}/api/auth/`
      return axios.post(
        url,
        {
          code: this.$route.query.code
        },
        {
          headers: {'X-CSRFToken': Cookies.get('csrftoken')}
        }).then((response) => {
        if (response.data.done) {
          // console.log(response.data.data)
          this.uid = response.data.data.password
          const url = `${API_URL}/api/profile/?who=${response.data.data.email}&pass=${response.data.data.password}`
          return axios.get(
            url,
            {
              headers: {}
            }).then((response) => {
            this.showRoller = false
            // console.log(response.data)
            if (response.data.user.length > 0) {
              this.activeName = response.data.data.username
              this.activeUser = response.data.data.email
              this.loginsess = true
              this.logoutsess = false
              // this.$emit('message', {'a': true, 'b': false, 'c': response.data.data.username, 'd': response.data.data.email})
            } else {
              this.$notify({
                type: 'error',
                group: 'foo',
                title: 'ERROR',
                duration: 5000,
                text: response.data.mes
              })
            }
          })
        } else {
          this.$notify({
            type: 'error',
            group: 'foo',
            title: 'ERROR',
            duration: 5000,
            text: response.data.msg
          })
        }
      })
    },
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
