#!/usr/bin/env groovy

import jenkins.model.*
import hudson.tools.*
import com.cloudbees.jenkins.plugins.customtools.*
import com.synopsys.arc.jenkinsci.plugins.customtools.versions.ToolVersionConfig


CustomTool.DescriptorImpl descriptor = Jenkins.instance.getDescriptorByType(com.cloudbees.jenkins.plugins.customtools.CustomTool.DescriptorImpl.class)

String name = 'NodeJS_424'
String home = ''
String exportedPaths = '**/bin'

List<ToolInstaller> installers = new ArrayList<ToolInstaller>()
installers.add(new ZipExtractionInstaller('', 'https://nodejs.org/dist/v4.2.4/node-v4.2.4-linux-x64.tar.gz', ''))

List<ToolProperty> properties = new ArrayList<ToolProperty>()
properties.add(new InstallSourceProperty(installers))

List<CustomTool> installations = descriptor.getInstallations().toList()

// remove existing custom tool with same name
List<CustomTool> toRemove = new ArrayList<CustomTool>()
for (CustomTool tool : installations) {
  if (tool.getName().equals(name)) {
    toRemove.add(tool)
  }
}
installations.removeAll(toRemove);

// add custom tool
installations.add(new CustomTool(name, home, properties, exportedPaths, null, ToolVersionConfig.DEFAULT, null))

def customTools = installations as CustomTool[]
descriptor.setInstallations(customTools)
descriptor.save()