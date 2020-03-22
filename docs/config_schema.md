# Configuration
The code generation processes can be configured by a configuration file.
The following picture displays the possible configurations

```plantuml
class Job {
    StringType name 
    StringType description 
    Model[] models 
    Task[] tasks 
}

note top: base object that describes a\ncomplete code generation process
class Model {
    StringType jsonSchema 
    StringType nameSpace 
    BlackWhiteListEntry[] blackListed 
    BlackWhiteListEntry[] whiteListed 
}

note top: A model that should be\nused
class Task {
    StringType name 
    StringType description 
    BlackWhiteListEntry[] blackListed 
    BlackWhiteListEntry[] whiteListed 
    SingleFileTask singleFileTask 
    MultiFileTask multiFileTask 
}

note top: A task to run
class BlackWhiteListEntry {
    StringType name 
    BlackWhiteListEntryTypeEnum type 
}

note top: entry of a type back/white\nlist
class BlackWhiteListEntryTypeEnum {
}

class SingleFileTask {
    StringType template 
    StringType destFile 
    TemplateParam[] templateParams 
}

note top: parameter of a code generation\ntask that creates one file
class TemplateParam {
    StringType name 
    StringType value 
}

note top: additional, template specific custom parameter\nfor codegen task
class MultiFileTask {
    StringType template 
    StringType destDir 
    StringType destFilePrefix 
    StringType destFilePostfix 
    StringType destFileExt 
    TemplateParam[] templateParams 
}

note top: parameter of a code generation\ntask that creates one file\nper model type

    
Job "0" *-- "n" Model        
            
Job "0" *-- "n" Task        
            
    
Model "0" *-- "n" BlackWhiteListEntry        
            
    
Task "0" *-- "n" BlackWhiteListEntry        
            
Task  *--  SingleFileTask        
            
Task  *--  MultiFileTask        
            
    
BlackWhiteListEntry  *--  BlackWhiteListEntryTypeEnum        
            
    
    
SingleFileTask "0" *-- "n" TemplateParam        
            
    
    
MultiFileTask "0" *-- "n" TemplateParam        
            

footer \ngenerated with yacg (https://github.com/OkieOth/yacg),\npowered by plantuml (https://plantuml.com/)
```