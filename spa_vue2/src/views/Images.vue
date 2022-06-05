<template>
  <div class="text-center">
    
    <!-- --------------------------------------------------------- -->
    <v-container class="text-center my-4">
      <v-btn 
        dark
        small
        class="purple darken-4 mx-4"
        min-width="100"
        @click="dialogUpload = !dialogUpload"
        >Upload</v-btn>

      <v-btn 
        v-if="selectedImages.length"
        dark
        small
        class="purple darken-4 mx-4"
        min-width="100"
        @click="dialogDelete = !dialogDelete"
        >Delete</v-btn>
    </v-container>

    <!-- --------------------------------------------------------- -->
    <v-hover 
      v-for="(thumb, idx) in data" :key="idx"
      v-slot="{ hover }" 
    >
      <v-sheet
        :elevation="hover ? 6 : 2"
        :class="{ 'on-hover': hover, 'blue lighten-5': is_selected(idx) }"
        class="pa-2 ma-3 d-inline-flex"
        style="cursor:pointer;"
        width="140"
        height="140"
        @click="switch_selected(idx)"
      >
        <v-img
          :src="get_stream_url(idx)"
          contain
        >
          <template v-slot:placeholder>
            <v-row
              class="fill-height ma-0"
              align="center"
              justify="center"
            >
              <v-progress-circular
                indeterminate
                color="purple"
              ></v-progress-circular>
            </v-row>
          </template>
        </v-img>
      </v-sheet>
    </v-hover>
  
    <!-- --------------------------------------------------------- -->
    <v-dialog
      v-model="dialogDelete"
      max-width="500px"
    >
      <v-card class="pb-6">
        <v-card-title class="purple darken-3 white--text mb-6">
          Delete selected ({{selectedImages.length}}) images?
        </v-card-title>
        <v-card-actions>
          <v-container class="text-center">
            <v-btn
              dark 
              class="purple darken-3 mx-4" 
              min-width="120"
              type="submit"
              @click="submit_images_delete"
            >Ok</v-btn>
            <v-btn
              dark 
              class="grey darken-1 mx-4"
              min-width="120"
              type="button"
              @click="dialogDelete = !dialogDelete"
            >Cancel</v-btn>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- --------------------------------------------------------- -->

  <!-- --------------------------------------------------------- -->
  </div>
</template>


<script>
  // import HelloWorld from '../components/HelloWorld'
  import axios from 'axios'
  import { mapMutations } from 'vuex'

  export default {
    name: 'Images',
    data: () => ({
      title: "Images",
      streamBase: "/api/stream/",
      data:[],
      selectedImages: [],
      acts:[
        {
          title: "anything",
        },
        {
          title: "delete",
        }
      ],
      dialogUpload: false,
      dialogDelete: false
    }),
    components: {
      
    },
    methods:{
      ...mapMutations([ "set_err", "reset_err" ]),

      call_thumbs(){
        axios.get( "/api/thumbs", this.$store.getters.create_bearer_auth_header)
        .then((res)=>{
          console.log(res.data)
          this.data = res.data
        })
        .catch((err)=>{
          // console.log(err.message)
          this.set_err(err.message)
        })
      },

      get_stream_url(idx){
        let url = this.streamBase + this.data[idx]._id
        return url
      },

      is_selected(idx){
        if(this.selectedImages.includes(this.data[idx]._id)){
          return true
        }
        else return false
      },

      switch_selected(idx){
        if( this.selectedImages.includes(this.data[idx]._id) ){
          let delIdx = this.selectedImages.indexOf(this.data[idx]._id)
          this.selectedImages.splice(delIdx, 1)
        }
        else{
          this.selectedImages.push(this.data[idx]._id)
        }
      },

      async submit_images_delete(){
        let toRemove = {...this.selectedImages}
        for(let idx in toRemove){
          try{
            await axios.delete( "/api/image/"+toRemove[idx], this.$store.getters.create_bearer_auth_header)
          }
          catch(err){
            toRemove.splice(toRemove.indexOf(),1)
            this.set_err(err.message)
          } 
        }

        for(let idx in toRemove){
          await this.remove_image_item_by_id(toRemove[idx])
        }

        this.dialogDelete = !this.dialogDelete
      },

      async remove_image_item_by_id(id){
        const item = this.data.find(thumb => thumb._id === id)
        this.data.splice(this.data.indexOf(item), 1)
        this.selectedImages.splice(this.selectedImages.indexOf(id), 1)
      }

      
    },
    mounted: function(){
      this.call_thumbs()
    }
  }
</script>