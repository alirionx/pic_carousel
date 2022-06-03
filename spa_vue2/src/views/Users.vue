<template>
  <div>
    <v-card class="ma-6 mt-10 pa-4 elevation-6">
      <!-- <v-card-title class="purple darken-3 white--text py-1 px-4 subtitle-1 ">Users -->
      <v-card-title class="py-2 px-3 text-h7 ">Users</v-card-title>
      <v-data-table
        :headers="tableHeaders"
        :items="usersData"
        :search="search"
      >
        <template v-slot:item.act="{item}">
          <v-btn light icon @click="open_dialog(usersData.indexOf(item))">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </template>
      
      </v-data-table>
    </v-card>
  
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
      scrollable
      >
      <v-card tile>
        <form @submit.prevent="submit_user_edit">
        <v-toolbar flat dark color="purple darken-3" >
          <v-btn icon dark @click="close_dialog(cancel=true)" type="button">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>User Settings</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn icon dark type="submit">Save</v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-card-text>
            <v-text-field class="pa-3 mx-8 mt-10" required label="Username" v-model="editData.username" ></v-text-field>
            <v-select class="pa-3 mx-8" required label="Role" v-model="editData.role" :items="ddRoles"></v-select>
            <v-text-field class="pa-3 mx-8" required label="Email" v-model="editData.email" type="email"></v-text-field>
            <v-text-field class="pa-3 mx-8" label="Firstname" v-model="editData.firstname" ></v-text-field>
            <v-text-field class="pa-3 mx-8" required label="Lastname" v-model="editData.lastname" ></v-text-field>
        </v-card-text>

        </form>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
  // import HelloWorld from '../components/HelloWorld'
  import axios from 'axios'

  import { mapMutations } from 'vuex'

  export default {
    name: 'Users',
    data: () => ({
      title: "Users",
      tableHeaders: [
        { text: 'Username', value: 'username' },
        { text: 'Role', value: 'role' },
        { text: 'Email', value: 'email' },
        { text: 'Firstname', value: 'firstname' },
        { text: 'Lastname', value: 'lastname' },
        { text: 'Action', value: 'act' },
      ],
      search: null,
      usersData: [],
    
      editData:{
        _id: null,
        username: null,
        role: null,
        email: null,
        firstname: null,
        lastname: null
      },
      resetData:{},

      ddRoles:[
        {
          text: "Administrator",
          value: "admin"
        },
        {
          text: "User",
          value: "user"
        },
        {
          text: "Penner",
          value: "penner"
        }
      ],
      
      dialog: false,
      dialogIdx: null

    }),
    components: {
      
    },
    methods:{
      ...mapMutations([ "set_err", "reset_err" ]),

      call_users_data(){
        axios.get("/api/users", this.$store.getters.create_bearer_auth_header)
        .then((res)=>{
          // console.log(res.data)
          this.usersData = res.data

        })
        .catch((err)=>{
          // console.log(err.message)
          this.set_err(err.message)
        })
      },

      open_dialog(idx){
        this.dialog = true
        this.dialogIdx = idx
        this.editData = this.usersData[idx]
        this.resetData = {...this.usersData[idx]}
      },
      close_dialog(cancel=false){
        if(cancel){
          for(let prop in this.resetData){
            this.editData[prop] = this.resetData[prop]
          }
        }
        this.dialog = false
        this.dialogIdx = null
        this.resetData = {}
      },


      submit_user_edit(){
        axios.put(
          "/api/user/"+this.editData._id, 
          this.editData,
          this.$store.getters.create_bearer_auth_header
        )
        .then((res)=>{
          console.log(res.status)
          this.close_dialog()
        })
        .catch((err)=>{
          this.set_err(err.message)
          this.close_dialog(true)
        })
      },

    },
    mounted: function(){
      this.call_users_data()
    }
  }
</script>


<style >
.v-data-table th {
  padding-top:30px !important;
  font-size: 14px !important;
}
.v-data-table td {
  font-size: 15px !important;
}
.v-data-table tr:hover {
  background-color: transparent !important;
}
</style>