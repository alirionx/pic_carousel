<template>
  <v-card class="pa-4 ma-4 elevation-4">
    <!-- {{title}} -->
    <v-data-table
      :headers="headers"
      :items="data"
      :items-per-page="10"
      class="elevation-1"
    ></v-data-table>
    <!-- <table>
      <tr>
        <th v-for="(item,idx) in headers" :key="idx">{{item.text}}</th>
      </tr>
    </table> -->
  </v-card>
</template>

<script>
import axios from 'axios'
import { defineComponent } from 'vue';

// Components
// import HelloWorld from '../components/HelloWorld.vue';

export default defineComponent({
  name: 'Users',
  data: () =>({
    title: 'Users',
    headers: [
      { text: 'Username', value: 'username' },
      { text: 'Role', value: 'role' },
      { text: 'Email', value: 'email' },
      { text: 'Firstname', value: 'firstname' },
      { text: 'Lastname', value: 'lastname' },
    ],
    data: []
  }),
  components: {
  
  },

  methods:{
    get_users_data(){
      axios.get(
        "/users", 
        { headers: { Authorization: `Bearer ${this.$store.state.bearer}` }  }
      ).then( (resp) =>{
        console.log(resp.data);
        this.data = resp.data;
      })
    }
  },

  mounted: function(){
    this.get_users_data()
  }
  
});
</script>