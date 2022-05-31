<template>
    <v-card class="ma-6 mt-10 elevation-4">
    <v-card-title class="purple darken-3 white--text py-1 px-4 subtitle-1 ">Users
      <!-- <v-sheet class="pr-16">Users</v-sheet>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field> -->
    </v-card-title>
    <v-data-table
      :headers="tableHeaders"
      :items="tableData"
      :search="search"
    >
      <template v-slot:item.act>
        <v-menu bottom left >
            <template v-slot:activator="{ on, attrs }">
              <v-btn light icon v-bind="attrs" v-on="on" >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-item v-for="(act, idx) in acts" :key="idx" @click="call_act(idx)">
                <v-list-item-title>{{ act.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
      </template>
    
    </v-data-table>
  </v-card>
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
        { text: 'act', value: 'act' },
      ],
      tableData: [],
      search:null,
      acts: [
        { title: "edit" },
        { title: "set password" },
        { title: "delete" }
      ],
    }),
    components: {
      
    },
    methods:{
      ...mapMutations([ "set_err", "reset_err" ]),

      call_users_data(){
        let headers = {headers: { Authorization: `Bearer ${this.$store.state.bearer}` }}
        axios.get("/api/users", headers)
        .then((res)=>{
          // console.log(res.data)
          this.tableData = res.data

        })
        .catch((err)=>{
          // console.log(err.message)
          this.set_err(err.message)
        })
      },

      call_act(idx){
        console.log(idx)
        // console.log(act.title + ':', this.tableData[idx].username)
      }
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
</style>