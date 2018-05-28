from conans import ConanFile, CMake, tools


class JsonschemavalidatorConan(ConanFile):
    name = "json-schema-validator"
    version = "0.1"
    license = "MIT"
    url = "https://github.com/Myna65/json-schema-validator-conan-recipe"
    description = "<Description of Jsonschemavalidator here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "jsonformoderncpp/3.1.2@vthiery/stable"

    def source(self):
        self.run("git clone https://github.com/pboettch/json-schema-validator")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("json-schema-validator/CMakeLists.txt", "project(json-schema-validator CXX)",
                              '''project(json-schema-validator CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="json-schema-validator")
        cmake.build()
        cmake.test()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include", src="json-schema-validator/src")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["json-schema-validator"]
