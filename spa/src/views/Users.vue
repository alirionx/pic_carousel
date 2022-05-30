<template>
  <v-card class="pa-4 ma-4 elevation-4">
    {{title}}
    <v-table>
      <thead>
        <tr>
          <th class="text-left" v-for="(item,idx) in headers" :key="idx">{{item.text}}</th>
          <th class="text-center">Act</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row,idx) in data" :key="idx">
          <td class="text-left" v-for="(col,idx2) in headers" :key="idx2">{{row[col.value]}}</td>
          <td class="text-center">
            <v-btn icon >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
        </td>
        </tr>
      </tbody>
    </v-table>
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
    data: [],
    acts: [
      { text: "edit" },
      { text: "set password" },
      { text: "delete" }
    ],
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