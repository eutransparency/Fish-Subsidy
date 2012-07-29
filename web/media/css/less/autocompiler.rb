require '/Library/Ruby/Gems/1.8/gems/rb-fsevent-0.9.1/lib/rb-fsevent'

fsevent = FSEvent.new
fsevent.watch Dir.pwd do |directories|
  puts "Detected change inside: #{directories.inspect}"
  system 'make'
end
fsevent.run

# class PwdMaker < FSEvent
#     def on_change(directories)
#         puts "Detected change in: #{directories.inspect}"
#         system 'make'
#     end
# end
# 
# autocompiler = PwdMaker.new
# autocompiler.watch_directories [Dir.pwd]
# autocompiler.start
