<template>
  <div id="dashcont">
    <div v-if="showList" class="col-lg-12">
      <div class="col-md-3">
      </div>
      <div class="col-md-6" style="color: #122b40;">
        <div class="card" style="background: #fff; border-radius: 10px; padding: 20px;">
          <div style="border-bottom: 2px solid #122b40;">
          <h1 style="text-align: center;">{{config.alias}}</h1>
          </div>
          <div id="formz">
            <div id="chat-box" style="width: 100%; height: 350px; overflow-y: auto; padding-top: 10px;">
              <table style="width: 100%; padding: 0px; margin: 0px;">

                <tr v-for="(chat, k) in chats" :key="k">
                  <td v-if="chat.who === 'bot'" colspan="1" style="width: 50%; padding-bottom: 20px;">
                    <div style="padding: 5px; border: 1px solid #122b40; background: #eee; width: 100%; border-radius: 0 10px 10px 10px;">
                      <p style="font-size: 80%; color: #122b40; font-weight: bold;" v-html="chat.mes"></p>
                      <small style="color: green; font-weight: bold; font-size: 60%;">{{chat.time}}</small>
                    </div>
                  </td>
                  <td v-if="chat.who === 'bot'" colspan="1" style="width: 50%; padding-bottom: 20px;"></td>

                  <td v-if="chat.who === 'user'" colspan="1" style="width: 50%; padding-bottom: 20px;"></td>
                  <td v-if="chat.who === 'user'" colspan="1" style="width: 50%; padding-bottom: 20px;">
                    <div style="padding: 5px; border: 1px solid #122b40; background: #122b40; width: 100%; border-radius: 10px 0px 10px 10px; ">
                      <p style="font-size: 80%; color: #fff; font-weight: bold;" v-html="chat.mes"></p>
                      <small style="color: green; font-weight: bold; font-size: 60%;">{{chat.time}}</small>
                    </div>
                  </td>
                </tr>

              </table>
            </div>

            <div class="form-group">
              <div class="card" style="padding: 10px;">
                <table style="width: 100%; padding: 0px;">
                  <tr>
                    <td style="width: 90%">
                      <textarea class="form-control" v-model="chat" placeholder="Enter BOT Commands" minlength="10" rows="2"
                          cols="50" style="resize: none; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-right: 0px solid #fff;"></textarea>
                    </td>
                    <td style="width: 10%">
                      <span v-on:click="submitList" class="btn btn-default btn-lg"
                      style="color: #fff; background: #122b40; font-weight: bolder; padding-top: 24px; padding-bottom: 24px; border-top-left-radius: 0px; border-bottom-left-radius: 0px; border-left: 0px solid #fff;"><rarr v-if="submitBt"></rarr><spinner v-if="submitSpinner"></spinner></span>
                    </td>
                  </tr>
                </table>

              </div>
            </div>

          </div>
        </div>
      </div>
      <div class="col-md-3"></div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
const API_URL = 'http://128.199.12.188:8000'
var d = new Date()
var hr = ''
var mn = ''
var sc = ''
var zo = 'PM'
if (String(d.getHours()).length === 1) {
  hr = '0' + String(d.getHours())
  zo = 'AM'
} else {
  hr = String(d.getHours())
}
if (String(d.getMinutes()).length === 1) {
  mn = '0' + String(d.getMinutes())
} else {
  mn = String(d.getMinutes())
}
if (String(d.getSeconds()).length === 1) {
  sc = '0' + String(d.getSeconds())
} else {
  sc = String(d.getSeconds())
}
var time = hr + ':' + mn + ':' + sc + zo
export default {
  name: 'Dashboard',
  components: {},
  props: ['activeUser', 'activeName', 'showList', 'hideList'],
  create () {
    // console.log(this.showList)

  },
  data () {
    return {
      chats: [
        {
          who: 'bot',
          mes: 'Welcome @' + this.activeName + ', what can I do for you today?',
          time: time
        }
      ],
      submitBt: true,
      submitSpinner: false,
      chat: '',
      config: {
        alias: ''
      }
    }
  },
  created () {
    this.fetchConfig(this.activeUser)
    this.fetchTimer(this.activeUser)
    // setInterval(() => {
    //   this.fetchConfig(this.activeUser)
    // }, 5000)
    setInterval(() => {
      this.fetchTimer(this.activeUser)
    }, 5000)
  },
  methods: {
    onChange (event) {
      this.category = event.target.value
    },
    fetchConfig (who) {
      const url = `${API_URL}/api/config/?who=${who}`
      return axios.get(
        url,
        {
          headers: {}
        }).then((response) => {
        // console.log(response.data)
        if (response.data.done) {
          this.config = response.data.data
        }
      })
    },
    fetchTimer (who) {
      const url = `${API_URL}/api/timer/?who=${who}`
      return axios.get(
        url,
        {
          headers: {}
        }).then((response) => {
        // console.log(response.data)
        if (response.data.done && response.data.data.length > 0) {
          var x = 0
          var cts = response.data.data
          for (x in cts) {
            var d = new Date()
            var hr = ''
            var mn = ''
            var sc = ''
            var zo = 'PM'
            if (String(d.getHours()).length === 1) {
              hr = '0' + String(d.getHours())
              zo = 'AM'
            } else {
              hr = String(d.getHours())
            }
            if (String(d.getMinutes()).length === 1) {
              mn = '0' + String(d.getMinutes())
            } else {
              mn = String(d.getMinutes())
            }
            if (String(d.getSeconds()).length === 1) {
              sc = '0' + String(d.getSeconds())
            } else {
              sc = String(d.getSeconds())
            }
            var time = hr + ':' + mn + ':' + sc + zo
            var put = {
              who: 'bot',
              mes: cts[x].content,
              time: time
            }
            setTimeout(() => {
              this.chats[this.chats.length] = put
              var cha = this.chat
              this.chat = ' '
              this.chat = cha
              // console.log(this.chats)
            }, 1000)
            setTimeout(() => {
              var container = this.$el.querySelector('#chat-box')
              container.scrollTop = container.scrollHeight
            }, 1500)
          }
        }
      })
    },
    submitList () {
      this.submitBt = false
      this.submitSpinner = true
      if (this.chat.length > 0) {
        var d = new Date()
        var hr = ''
        var mn = ''
        var sc = ''
        var zo = 'PM'
        if (String(d.getHours()).length === 1) {
          hr = '0' + String(d.getHours())
          zo = 'AM'
        } else {
          hr = String(d.getHours())
        }
        if (String(d.getMinutes()).length === 1) {
          mn = '0' + String(d.getMinutes())
        } else {
          mn = String(d.getMinutes())
        }
        if (String(d.getSeconds()).length === 1) {
          sc = '0' + String(d.getSeconds())
        } else {
          sc = String(d.getSeconds())
        }
        var time = hr + ':' + mn + ':' + sc + zo
        this.chats[this.chats.length] = {
          who: 'user',
          mes: this.chat,
          time: time
        }
        var ct = this.chat
        this.chat = ''
        setTimeout(() => {
          var container = this.$el.querySelector('#chat-box')
          container.scrollTop = container.scrollHeight
        }, 500)
        const url = `${API_URL}/api/chat/`
        return axios.post(
          url,
          {
            email: this.activeUser,
            command: ct,
            config: this.config
          },
          {
            headers: {
              'X-CSRFToken': Cookies.get('csrftoken')
            }
          }).then((response) => {
          // console.log(response.data)
          this.submitBt = true
          this.submitSpinner = false
          if (response.data.done) {
            this.config = response.data.config
            if (response.data.showmes === true) {
              var d = new Date()
              var hr = ''
              var mn = ''
              var sc = ''
              var zo = 'PM'
              if (String(d.getHours()).length === 1) {
                hr = '0' + String(d.getHours())
                zo = 'AM'
              } else {
                hr = String(d.getHours())
              }
              if (String(d.getMinutes()).length === 1) {
                mn = '0' + String(d.getMinutes())
              } else {
                mn = String(d.getMinutes())
              }
              if (String(d.getSeconds()).length === 1) {
                sc = '0' + String(d.getSeconds())
              } else {
                sc = String(d.getSeconds())
              }
              var time = hr + ':' + mn + ':' + sc + zo
              this.chats[this.chats.length] = {
                who: 'bot',
                mes: response.data.msg,
                time: time
              }
            }
            setTimeout(() => {
              var container = this.$el.querySelector('#chat-box')
              container.scrollTop = container.scrollHeight
            }, 500)
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
      } else {
        this.submitBt = true
        this.submitSpinner = false
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'Oops! You can\'t send an empty command'
        })
      }
    }
  }
}
</script>
<style scoped>
  .form-group {
    text-align: left;
  }
</style>
