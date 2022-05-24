<template>
  <v-container
    class="d-flex align-center justify-center mt-16"  
  >
  <form @submit.prevent="submit">
  <v-card
    class="elevation-10 pa-6"  
    min-height="250"
    width="60vh"
  >
    <v-toolbar color="purple darken-4" class="mb-6 ">
      <v-toolbar-title>Login</v-toolbar-title>
    </v-toolbar>

    <v-text-field
      prepend-icon="mdi-account"
      class="px-3"
      variant="underlined"
      v-model="payload.username"
      label="Username"
      required
    ></v-text-field>

    <v-text-field
      prepend-icon="mdi-lock"
      class="px-3"
      variant="underlined"
      v-model="payload.password"
      label="Password"
      required
      type="password"
    ></v-text-field>

    <v-container class="text-center mb-3 pa-0">
      <v-btn
        color="purple darken-4"
        min-width="120px"
        type="submit"
      >Login</v-btn>
    </v-container>

  </v-card>
  </form>
  </v-container>


</template>

<script>
import axios from 'axios'
import { defineComponent } from 'vue';

// Components
// import HelloWorld from '../components/HelloWorld.vue';

export default defineComponent({
  name: 'Login',
  data: () =>({
    title: 'Login',
    payload:{
      username: null,
      password: null
    }
  }),
  components: {
  
  },
  methods:{
    submit(){
      // console.log(this.payload )
      const params = new URLSearchParams();
      for(let prop in this.payload){
        params.append(prop, this.payload[prop])
      }
      axios.post('/auth', params )
      .then(response => { 
        //this.loader = false;
        // console.log(response.data.access_token);
        this.$store.dispatch("set_bearer", response.data.access_token)//.then( console.log(this.$store.state.bearer))
        this.$router.push('/')
      })
      .catch(error => {
        // console.log(error);
        // context.commit('reset_bearer');
        this.payload.username = null;
        this.payload.password = null;
      });
    }
  }
  
});
</script>
