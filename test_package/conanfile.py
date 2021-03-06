#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os
import platform


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def imports(self):
        for p in  self.deps_cpp_info.bin_paths:
            filename = os.path.join( p,'plugin.node')
            print(filename,'<=============================',os.path.exists( filename ))
            
            if os.path.exists( filename ):
                self.copy('plugin.node',dst='bin',src=p)
                self.copy('case-converter-plugin%s'%self._EXT(),dst='bin',src=p)

    #def build(self):
    #    cmake = CMake(self)
    #    cmake.configure()
    #    cmake.build()

    def test(self):
        


        
        with tools.environment_append(RunEnvironment(self).vars):
            command ='node test.js {0}/bin/plugin.node {0}/bin/case-converter-plugin{1}'.format(
                os.path.abspath('.'), self._EXT())

            self.run(command,cwd = os.path.dirname(__file__))


    def _EXT(self):
        if self.settings.os == "Windows":
            return '.dll'
        elif self.settings.os == "Macos":
            return '.dylib'
        else: # Linux
            return '.so'

