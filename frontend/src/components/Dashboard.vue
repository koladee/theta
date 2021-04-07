<template>
  <div id="dashcont">
    <div v-if="showSettings" class="col-lg-12">
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
    <div v-if="hideSettings" class="col-lg-12">
      <div class="col-md-2"></div>
      <div class="col-md-8">
        <div class="card" style="background: #fff; width: 100%; min-height: 300px; padding: 20px;">
          <div class="row">
            <div class="col-md-12">
              <div class="card" style="width: 100%; min-height: 300px; padding: 20px;">
                <center><h3 style="color: #122b40; font-weight: bold;">CONFIGURE A NEW LEVEL REWARD</h3></center>
              <br>
                <div class="col-md-6">
                  <div class="form-group">
                    <label style="color: #122b40; font-weight: bold;">LEVEL:</label>
                    <input v-model="newLevel" type="number" min="1" max="100" placeholder="Level Number (1-100)" class="form-control" style="color: #122b40; font-weight: bold;"/>
                  </div>
                </div>
                <div class="col-md-6">
                  <label style="color: #122b40; font-weight: bold;">EMOTES & REWARDS:</label>
                  <div  id="emotes-cont" style="width: 100%; height: 100px; padding: 10px; overflow-y: auto;">
                    <div v-for="(emote, k) in emotes" :key="k" v-on:click="pick_emote(emote.id, '-new')" :id="'emote-'+emote.id+'-box-new'" class="card" style="cursor: pointer; height: 50px;">
                      <table>
                        <tr>
                          <td style="width: 20%;">
                            <!--forge_items id (emote id)-->
                            <!--forge_items metadata image_urls large (image src)-->
                            <!--forge_items metadata name (emote name)-->
                            <!--forge_items metadata code ":SubwaySubshappytoast:"-->
                            <img style="height: 50px; width: 50px; border-radius: 10px 0px 10px 0px;" :src="emote.metadata.image_urls.large" alt=" "/>
                          </td>
                          <td style="width: 80%;">
                            <div style="padding-left: 20px; padding-right: 20px; text-align: center;">
                            <span style="font-weight: bolder; color: #122b40; font-size: 100%;">{{emote.metadata.name}}</span>
                            <br>
                            <span class="label label-info" style="font-weight: bold; background: #122b40; color: #ffffff; font-size: 80%;">{{emote.metadata.code}}</span>
                          </div>
                          </td>
                        </tr>
                      </table>
                    </div>
                  </div>
                </div>
                <div class="col-md-12" style="padding-top: 20px;">
                  <div class="form-group" style="text-align: center;">
                    <span v-on:click="new_reward" class="btn btn-primary" style="font-weight: bold;"><span v-if="!newLevelSpinner">CONFIGURE</span><spinner v-if="newLevelSpinner"></spinner></span>
                  </div>
                </div>
              </div>

              <div class="card" style="width: 100%; min-height: 600px; padding: 20px; margin-top: 50px;">
                <center><h3 style="color: #122b40; font-weight: bold;">MANAGE REWARDS</h3></center>
                <br>
                <div class="col-md-12" style="width: 100%; max-height: 500px; overflow-y: auto; overflow-x: auto;">
                  <table class="table table-bordered table-responsive table-hover table-striped">
                    <thead>
                      <tr>
                        <th>&numero;</th>
                        <th>LEVEL</th>
                        <th>EMOTE/REWARD</th>
                        <th>CREATED DATE</th>
                        <th>ACTIONS</th>
                      </tr>
                    </thead>

                    <tbody style="width: 100%; max-height: 500px; overflow-y: auto;">
                      <tr v-for="(reward, k) in myRewards" :key="k" :id="'row-'+String(k)">
                        <td>{{k+1}}</td>
                        <td style="text-align: center;">
                          <span class="label label-success">{{reward.level}}</span>
                        </td>
                        <td>
                          <div v-for="(emote, k) in emotes" :key="k" v-if="emote.id === reward.reward" class="card" style="cursor: pointer; height: 50px;">
                            <table>
                              <tr>
                                <td style="width: 20%;">
                                  <!--forge_items id (emote id)-->
                                  <!--forge_items metadata image_urls large (image src)-->
                                  <!--forge_items metadata name (emote name)-->
                                  <!--forge_items metadata code ":SubwaySubshappytoast:"-->
                                  <img style="height: 50px; width: 50px; border-radius: 10px 0px 10px 0px;" :src="emote.metadata.image_urls.large" alt=" "/>
                                </td>
                                <td style="width: 80%;">
                                  <div style="padding-left: 20px; padding-right: 20px; text-align: center;">
                                  <span style="font-weight: bolder; color: #122b40; font-size: 100%;">{{emote.metadata.name}}</span>
                                  <br>
                                  <span class="label label-info" style="font-weight: bold; background: #122b40; color: #ffffff; font-size: 80%;">{{emote.metadata.code}}</span>
                                </div>
                                </td>
                              </tr>
                            </table>
                          </div>
                        </td>
                        <td style="text-align: center;">
                          <span v-if="reward.created_date !== ''">
                            <span class="label label-info" v-html="reward.created_date.split('T')[0]"></span>
                          </span>
                        </td>
                        <td>
                          <span data-toggle="modal" data-target="#edit-reward-modal" v-on:click="edit_reward(String(k))" class="btn btn-primary btn-block">EDIT <i class="glyphicon glyphicon-edit"></i></span>
                          <br>
                          <span v-on:click="delete_reward(String(k), reward.reward)" :id="'delete-bt-'+String(k)" class="btn btn-danger btn-block">DELETE <i class="glyphicon glyphicon-trash"></i></span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-2"></div>
      <div class="modal fade" id="emotes-modal" tabindex="-1" role="dialog" aria-labelledby="Emotes" aria-hidden="true">
        <div class="modal-dialog modal-md">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true" style="color: #122b40;">&times;</button>
              <h4 class="modal-title" style="color: #122b40; font-weight: bold;">EMOTES' SETTINGS</h4>
            </div>
            <div class="modal-body"  style="min-height: 300px;">

            </div>
          </div>
        </div>
      </div>
      <div class="modal fade" id="edit-reward-modal" tabindex="-1" role="dialog" aria-labelledby="Emotes" aria-hidden="true">
        <div class="modal-dialog modal-md">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true" style="color: #122b40;">&times;</button>
              <h4 class="modal-title" style="color: #122b40; font-weight: bold;"><i class="glyphicon glyphicon-edit"></i> EDIT REWARD</h4>
            </div>
            <div class="modal-body"  style="min-height: 250px;">
              <div v-if="JSON.stringify(editedReward) !== JSON.stringify({})" class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label style="color: #122b40; font-weight: bold;">LEVEL:</label>
                    <input v-model="editedReward.level" type="number" min="1" max="100" placeholder="Level Number (1-100)" readonly class="form-control disabled" style="color: #122b40; font-weight: bold;"/>
                  </div>
                </div>
                <div class="col-md-6">
                  <label style="color: #122b40; font-weight: bold;">EMOTES & REWARDS:</label>
                  <div id="emotes-cont-edit" style="width: 100%; height: 100px; padding: 10px; overflow-y: auto;">
                    <div v-for="(emote, k) in emotes" :key="k" >
                      <div v-if="emote.id !== editedReward.reward" v-on:click="pick_emote(emote.id, '-edit')" :id="'emote-'+emote.id+'-box-edit'" class="card" style="cursor: pointer; height: 50px;">
                        <table>
                          <tr>
                            <td style="width: 20%;">
                              <!--forge_items id (emote id)-->
                              <!--forge_items metadata image_urls large (image src)-->
                              <!--forge_items metadata name (emote name)-->
                              <!--forge_items metadata code ":SubwaySubshappytoast:"-->
                              <img style="height: 50px; width: 50px; border-radius: 10px 0px 10px 0px;" :src="emote.metadata.image_urls.large" alt=" "/>
                            </td>
                            <td style="width: 80%;">
                              <div style="padding-left: 20px; padding-right: 20px; text-align: center;">
                                <span style="font-weight: bolder; color: #122b40; font-size: 100%;">{{emote.metadata.name}}</span>
                                <br>
                                <span class="label label-info" style="font-weight: bold; background: #122b40; color: #ffffff; font-size: 80%;">{{emote.metadata.code}}</span>
                              </div>
                            </td>
                          </tr>
                        </table>
                      </div>
                      <div v-if="emote.id === editedReward.reward" v-on:click="pick_emote(emote.id, '-edit')" :id="'emote-'+emote.id+'-box-edit'" class="card" style="cursor: pointer; height: 50px; background: red;">
                        <table>
                          <tr>
                            <td style="width: 20%;">
                              <!--forge_items id (emote id)-->
                              <!--forge_items metadata image_urls large (image src)-->
                              <!--forge_items metadata name (emote name)-->
                              <!--forge_items metadata code ":SubwaySubshappytoast:"-->
                              <img style="height: 50px; width: 50px; border-radius: 10px 0px 10px 0px;" :src="emote.metadata.image_urls.large" alt=" "/>
                            </td>
                            <td style="width: 80%;">
                              <div style="padding-left: 20px; padding-right: 20px; text-align: center;">
                                <span style="font-weight: bolder; color: #122b40; font-size: 100%;">{{emote.metadata.name}}</span>
                                <br>
                                <span class="label label-info" style="font-weight: bold; background: #122b40; color: #ffffff; font-size: 80%;">{{emote.metadata.code}}</span>
                              </div>
                            </td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-md-12" style="padding-top: 20px;">
                  <div class="form-group" style="text-align: center;">
                    <span v-on:click="save_edited_reward(editedReward.reward)" class="btn btn-primary" style="font-weight: bold;"><span v-if="!saveRewardEditSpinner">SAVE EDIT <i class="glyphicon glyphicon-saved"></i></span><spinner v-if="saveRewardEditSpinner"></spinner></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
const API_URL = 'https://mrnft.gg'
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
  props: ['uid', 'activeUser', 'activeName', 'showSettings', 'hideSettings'],
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
      },
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
      pickedEmote: '',
      newLevel: '',
      newLevelSpinner: false,
      myRewards: [],
      editedReward: {},
      saveRewardEditSpinner: false
    }
  },
  created () {
    this.fetchConfig(this.activeUser)
    this.fetchGifts()
    this.fetchRewards()
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
    pick_emote (a, b) {
      this.$el.querySelector('#emote-' + a + '-box' + b).setAttribute('style', 'cursor: pointer; height: 50px; background: red;')
      if (this.pickedEmote !== '') {
        const pkd = this.pickedEmote
        this.$el.querySelector('#emote-' + pkd + '-box' + b).setAttribute('style', 'cursor: pointer; height: 50px;')
        var put = ''
        if (this.pickedEmote === a) {
          put = ''
        } else {
          put = a
        }
        setTimeout(() => {
          this.pickedEmote = put
        }, 500)
      } else {
        setTimeout(() => { this.pickedEmote = a }, 500)
      }
    },
    new_reward () {
      this.newLevelSpinner = true
      setTimeout(() => {
        if (parseInt(this.newLevel) > 0 && parseInt(this.newLevel) <= 100) {
          if (this.pickedEmote !== '') {
            const url = `${API_URL}/api/reward/new/`
            return axios.post(
              url,
              {
                user_id: this.uid,
                level: this.newLevel,
                reward: this.pickedEmote,
                reward_type: 'item_forge'
              },
              {
                headers: {
                  'X-CSRFToken': Cookies.get('csrftoken')
                }
              }).then((response) => {
              // console.log(response.data)
              this.newLevelSpinner = false
              this.pick_emote(this.pickedEmote, '-new')
              this.newLevel = ''
              if (response.data.done) {
                if (typeof response.data.data !== 'undefined') {
                  this.myRewards = response.data.data
                  this.$notify({
                    type: 'success',
                    group: 'foo',
                    title: 'SUCCESS',
                    duration: 5000,
                    text: response.data.msg
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
            this.newLevelSpinner = false
            this.$notify({
              type: 'error',
              group: 'foo',
              title: 'ERROR',
              duration: 5000,
              text: 'You have to pick a reward or an emote for the specified level.'
            })
          }
        } else {
          this.newLevelSpinner = false
          this.$notify({
            type: 'error',
            group: 'foo',
            title: 'ERROR',
            duration: 5000,
            text: 'Level number is required and must be between 1 and 100.'
          })
        }
      }, 1000)
    },
    edit_reward (a) {
      this.editedReward = this.myRewards[parseInt(a)]
      setTimeout(() => {
        var container = this.$el.querySelector('#emotes-cont-edit')
        var e = 0
        for (e in this.emotes) {
          if (this.emotes[e].id === this.myRewards[parseInt(a)].reward) {
            this.pickedEmote = this.emotes[e].id
            break
          }
        }
        container.scrollTop = e * 70
      }, 500)
    },
    save_edited_reward (a) {
      setTimeout(() => {
        this.saveRewardEditSpinner = true
        const url = `${API_URL}/api/reward/edit/`
        return axios.post(
          url,
          {
            user_id: this.uid,
            level: this.editedReward.level,
            reward: this.pickedEmote,
            reward_type: 'item_forge'
          },
          {
            headers: {
              'X-CSRFToken': Cookies.get('csrftoken')
            }
          }).then((response) => {
          // console.log(response.data)
          // this.$el.querySelector('#edit-reward-modal').setAttribute('class', 'modal fade')
          // this.$el.querySelector('#edit-reward-modal').setAttribute('style', 'display: none;')
          this.saveRewardEditSpinner = false
          // this.pick_emote(this.pickedEmote, '-edit')
          if (response.data.done) {
            // close bootstrap modal here
            if (typeof response.data.data !== 'undefined') {
              this.myRewards = response.data.data
              this.$notify({
                type: 'success',
                group: 'foo',
                title: 'SUCCESS',
                duration: 5000,
                text: response.data.msg
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
      }, 500)
    },
    delete_reward (a, b) {
      var conf = confirm('Are you sure you want to delete this setting?')
      if (conf) {
        var level = this.myRewards[parseInt(a)].level
        this.myRewards.splice(a, 1)
        const url = `${API_URL}/api/reward/delete/`
        return axios.post(
          url,
          {
            user_id: this.uid,
            level: level
          },
          {
            headers: {
              'X-CSRFToken': Cookies.get('csrftoken')
            }
          }).then((response) => {
          // console.log(response.data)
          if (response.data.done) {
            this.$notify({
              type: 'success',
              group: 'foo',
              title: 'SUCCESS',
              duration: 5000,
              text: response.data.msg
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
      }
    },
    fetchGifts () {
      const url = `${API_URL}/api/giftable/get/`
      return axios.post(
        url,
        {
          user_id: this.uid
        },
        {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        }).then((response) => {
        // console.log(response.data)
        if (response.data.done) {
          if (response.data.data.length > 0) {
            this.emotes = response.data.data
          }
        }
      })
    },
    fetchRewards () {
      const url = `${API_URL}/api/rewards/`
      return axios.post(
        url,
        {
          user_id: this.uid
        },
        {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        }).then((response) => {
        console.log(response.data)
        if (response.data.done) {
          this.myRewards = response.data.data
        }
      })
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
        var dir = this.chat.substr(0, 1)
        if (dir === '/') {
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
            if (response.data.showmes === true || response.data.showmes === false) {
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
