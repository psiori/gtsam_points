from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout


class GtsamPointsConan(ConanFile):
    name = "gtsam_points"
    version = "1.2.2"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_with_cuda": [True, False],
        "build_with_march_native": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "build_with_cuda": False,
        "build_with_march_native": True,
    }
    exports_sources = "*"

    def requirements(self):
        self.requires("gtsam/4.3a1")
        self.requires("eigen/3.4.0")
        self.requires("boost/1.83.0")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_WITH_CUDA"] = self.options.build_with_cuda
        tc.variables["BUILD_WITH_MARCH_NATIVE"] = self.options.build_with_march_native
        tc.variables["BUILD_WITH_OPENMP"] = False
        tc.variables["BUILD_DEMO"] = False
        tc.variables["BUILD_TESTS"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = ["gtsam_points"]
        self.cpp_info.builddirs.append("lib/cmake/gtsam_points")
