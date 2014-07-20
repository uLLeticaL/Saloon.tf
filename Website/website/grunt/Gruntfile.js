module.exports = function(grunt) {
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    coffee: {
      compile: {
        files: {
          'js/app.js': [
            'coffee/*.coffee'
          ]
        }
      }
    },
    uglify: {
      dist: {
        files: {
          '../public/javascript.js': [
            'js/jquery.js',
            'js/plugins/*.js',
            'js/bootstrap/transition.js',
            'js/bootstrap/alert.js',
            'js/bootstrap/button.js',
            'js/bootstrap/carousel.js',
            'js/bootstrap/collapse.js',
            'js/bootstrap/dropdown.js',
            'js/bootstrap/modal.js',
            'js/bootstrap/tooltip.js',
            'js/bootstrap/popover.js',
            'js/bootstrap/scrollspy.js',
            'js/bootstrap/tab.js',
            'js/bootstrap/affix.js',
            'js/jasny/*.js',
            'js/app.js'
          ]
        },
        options: {
          banner: '/*! <%= pkg.name %>\'s JavaScript. Generated at <%= grunt.template.today("yyyy-mm-dd") %> */\n'
        }
      }
    },
    sass: {
      dist: {
        options: {
          style: "compresses",
          banner: '/*! <%= pkg.name %>\'s CSS. Generated at <%= grunt.template.today("yyyy-mm-dd") %> */\n'
        },
        files: {
          '../public/stylesheet.css': 'sass/styles.sass'
        }
      }
    },
    'string-replace': {
      dist: {
        src: '../templates/base.mako',
        dest: '../templates/base.mako',
        options: {
          replacements: [{
            pattern: /\?v=[0-9]+\.[0-9]+\.[0-9]+/g,
            replacement: '\?v=<%= pkg.version %>'
          }]
        }
      }
    }
  });

  // Load the plugin that provides the "coffee" task.
  grunt.loadNpmTasks('grunt-contrib-coffee');
  // Load the plugin that provides the "concat" task.
  //grunt.loadNpmTasks('grunt-contrib-concat');
  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  // Load the plugin that provides the "sass" task.
  grunt.loadNpmTasks('grunt-contrib-sass');
  // Load the plugin that provides the "version" task.
  grunt.loadNpmTasks('grunt-string-replace');

  // Default task(s).
  grunt.registerTask('default', ['coffee','uglify','sass','string-replace']);

};
