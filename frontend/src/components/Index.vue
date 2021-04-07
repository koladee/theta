<template>
  <div id="app-index">
    <div v-if="loginDiv" class="row hidden" style="margin: 0px; padding: 0px;">
      <div class="col-md-4"></div>
      <div class="col-md-4" style="padding-top: 7%;">
        <div class="card" style="padding: 20px; background: #fff; color: #122b40;">
          <center><h1 style="font-weight: bolder;">LOGIN</h1></center>
          <div class="form-group">
            <label>Email Address:</label>
            <input v-model="loginUser" type="email" class="form-control" placeholder="Email">
          </div>
          <div class="form-group">
            <label>Password:</label>
            <input v-model="loginPass" type="password" class="form-control" placeholder="Password">
          </div>
          <div class="form-group">
            <center>
              <span v-on:click="login" class="btn btn-default"
                    style="font-weight: bolder; padding: 10px; font-size: 120%;">{{loginBt}}<spinner
                v-if="loginSpinner"></spinner></span>
              <br>
              <span style="cursor: pointer;">Don't have an account? <a href="#" v-on:click="reg_form">Sign Up</a></span>
            </center>
          </div>
        </div>
      </div>
      <div class="col-md-4"></div>
    </div>
    <div v-if="regDiv" class="row" style="margin: 0px; padding: 0px;">
      <div class="col-md-3"></div>
      <div class="col-md-6" style="padding-top: 5%;">
        <div class="card" style="padding: 20px; background: #fff; color: #122b40;">
          <center><h1 style="font-weight: bolder;">SIGN UP</h1></center>
          <div class="form-group">
            <label>First Name:</label>
            <input v-model="regFname" type="text" class="form-control" placeholder="First Name">
          </div>
          <div class="form-group">
            <label>Last Name:</label>
            <input v-model="regLname" type="text" class="form-control" placeholder="Last Name">
          </div>
          <div class="form-group">
            <label>Username:</label>
            <input v-model="regUsername" type="text" class="form-control" placeholder="Username">
          </div>
          <div class="form-group">
            <label>Email Address:</label>
            <input v-model="regEmail" type="email" class="form-control" placeholder="Email Address">
          </div>
          <div class="form-group">
            <label>Password:</label>
            <input v-model="regPass" type="password" class="form-control" placeholder="Password">
          </div>
          <div class="form-group">
            <label>Confirm Password:</label>
            <input v-model="regPassConf" type="password" class="form-control" placeholder="Confirm Password">
          </div>
          <div class="form-group">
            <center>
              <span id="reg-bt" v-on:click="submitReg" class="btn btn-default"
                    style="font-weight: bolder; padding: 10px; font-size: 120%;">{{regBt}}<spinner
                v-if="regSpinner"></spinner></span>
              <br>
              <span style="cursor: pointer;">Already have an account? <a href="#" v-on:click="login_form">Login</a></span>
            </center>
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

const API_URL = 'https://mrnft.gg'
export default {
  name: 'Index',
  data () {
    return {
      loginBt: 'LOGIN',
      loginSpinner: false,
      loginDiv: true,
      regBt: 'SUBMIT',
      regSpinner: false,
      regDiv: false,
      loginUser: '',
      loginPass: '',
      regUsername: '',
      regFname: '',
      regLname: '',
      regEmail: '',
      regPass: '',
      regPassConf: ''
    }
  },
  methods: {
    login_form: function () {
      this.loginDiv = true
      this.regDiv = false
    },
    reg_form: function () {
      this.regDiv = true
      this.loginDiv = false
    },
    login: function () {
      this.loginBt = ''
      this.loginSpinner = true
      if (this.loginUser.length > 0) {
        if (this.loginPass.length > 0) {
          const url = `${API_URL}/api/profile/?who=${this.loginUser}&pass=${this.loginPass}`
          return axios.get(
            url,
            {
              headers: {}
            }).then((response) => {
            // console.log(response.data)
            this.loginBt = 'LOGIN'
            this.loginSpinner = false
            if (response.data.user.length > 0) {
              this.loginUser = ''
              this.loginPass = ''
              this.$emit('message', {'a': true, 'b': false, 'c': response.data.data.username, 'd': response.data.data.email})
              // this.$parent.loginsess = true
              // this.$parent.logoutsess = false
              // this.$parent.activeName = response.data.data.username
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
          this.loginBt = 'LOGIN'
          this.loginSpinner = false
          this.$notify({
            type: 'error',
            group: 'foo',
            title: 'ERROR',
            duration: 5000,
            text: 'Oops! The password field is required.'
          })
        }
      } else {
        this.loginBt = 'LOGIN'
        this.loginSpinner = false
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'Oops! The email field is required.'
        })
      }
    },
    submitReg: function () {
      this.regBt = ''
      this.regSpinner = true
      if (this.regFname.length > 0) {
        if (this.regLname.length > 0) {
          if (this.regUsername.length > 0) {
            if (this.regEmail.length > 0) {
              if (this.regPass === this.regPassConf && this.regPass.length > 0) {
                const url = `${API_URL}/api/profile/`
                return axios.post(
                  url,
                  {
                    email: this.regEmail,
                    username: this.regUsername,
                    password: this.regPass,
                    password2: this.regPassConf,
                    fname: this.regFname,
                    lname: this.regLname
                  },
                  {
                    headers: {
                      'X-CSRFToken': Cookies.get('csrftoken')
                    }
                  }).then((response) => {
                  // console.log(response.data)
                  this.regBt = 'SUBMIT'
                  this.regSpinner = false
                  if (response.data.done) {
                    this.regUsername = ''
                    this.regEmail = ''
                    this.regPass = ''
                    this.regPassConf = ''
                    this.regLname = ''
                    this.regFname = ''
                    this.$notify({
                      type: 'success',
                      group: 'foo',
                      title: 'SUCCESS',
                      duration: 5000,
                      text: 'Successfully signed up.'
                    })
                    this.login_form()
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
                this.regBt = 'SUBMIT'
                this.regSpinner = false
                this.$notify({
                  type: 'error',
                  group: 'foo',
                  title: 'ERROR',
                  duration: 5000,
                  text: 'Oops! Passwords do not match.'
                })
              }
            } else {
              this.regBt = 'SUBMIT'
              this.regSpinner = false
              this.$notify({
                type: 'error',
                group: 'foo',
                title: 'ERROR',
                duration: 5000,
                text: 'Oops! The email field is required.'
              })
            }
          } else {
            this.regBt = 'SUBMIT'
            this.regSpinner = false
            this.$notify({
              type: 'error',
              group: 'foo',
              title: 'ERROR',
              duration: 5000,
              text: 'Oops! A username is required.'
            })
          }
        } else {
          this.regBt = 'SUBMIT'
          this.regSpinner = false
          this.$notify({
            type: 'error',
            group: 'foo',
            title: 'ERROR',
            duration: 5000,
            text: 'Oops! Last name field is required.'
          })
        }
      } else {
        this.regBt = 'SUBMIT'
        this.regSpinner = false
        this.$notify({
          type: 'error',
          group: 'foo',
          title: 'ERROR',
          duration: 5000,
          text: 'Oops! First name field is required.'
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
