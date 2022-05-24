const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  },
  devServer: {
    proxy: {
      '/users': {
        target: 'http://localhost:5000',
        //pathRewrite: {'^/api' : ''}
      },
      '/auth': {
        target: 'http://localhost:5000',
        //pathRewrite: {'^/api' : ''}
      }
    }
  }

})
