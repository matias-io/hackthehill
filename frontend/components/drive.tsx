'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { FileIcon, FolderIcon, ImageIcon, Search, Plus, MoreVertical, UserCircle } from "lucide-react"

interface File {
  id: string
  name: string
  type: "file" | "folder" | "image"
  size: string
  modified: string
}

export default function Component() {
  const [files, setFiles] = useState<File[]>([
    { id: "1", name: "Document.docx", type: "file", size: "25 KB", modified: "2023-09-15" },
    { id: "2", name: "Images", type: "folder", size: "-- KB", modified: "2023-09-14" },
    { id: "3", name: "Project Files", type: "folder", size: "-- KB", modified: "2023-09-13" },
    { id: "4", name: "Screenshot.png", type: "image", size: "1.2 MB", modified: "2023-09-12" },
  ])
  const [newFileName, setNewFileName] = useState("")
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  const addNewFile = () => {
    if (newFileName) {
      const newFile: File = {
        id: (files.length + 1).toString(),
        name: newFileName,
        type: "file",
        size: "0 KB",
        modified: new Date().toISOString().split('T')[0],
      }
      setFiles([...files, newFile])
      setNewFileName("")
      setIsDialogOpen(false)
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-72 bg-white p-6 border-r border-gray-200 flex flex-col">
        <div className="flex items-center space-x-3 mb-8">
          <Avatar>
            <AvatarImage src="/placeholder-avatar.jpg" alt="User" />
            <AvatarFallback><UserCircle /></AvatarFallback>
          </Avatar>
          <div>
            <h2 className="font-semibold text-gray-800">John Doe</h2>
            <p className="text-sm text-gray-500">john@example.com</p>
          </div>
        </div>
        <Button className="w-full mb-6" onClick={() => setIsDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" /> New File
        </Button>
        <nav className="space-y-4 mb-8">
          <Button variant="ghost" className="w-full justify-start text-gray-600 hover:text-gray-800 hover:bg-gray-100">
            <FileIcon className="mr-3 h-4 w-4" /> My Files
          </Button>
          <Button variant="ghost" className="w-full justify-start text-gray-600 hover:text-gray-800 hover:bg-gray-100">
            <FolderIcon className="mr-3 h-4 w-4" /> Shared with me
          </Button>
        </nav>
        <div className="flex-grow overflow-auto">
          <h3 className="font-semibold text-gray-600 mb-4 text-sm uppercase tracking-wider">Your Files</h3>
          {files.map((file) => (
            <div key={file.id} className="flex items-center space-x-3 mb-4 text-gray-600 hover:text-gray-800">
              {file.type === "file" && <FileIcon className="h-4 w-4 text-blue-500" />}
              {file.type === "folder" && <FolderIcon className="h-4 w-4 text-yellow-500" />}
              {file.type === "image" && <ImageIcon className="h-4 w-4 text-green-500" />}
              <span className="text-sm truncate">{file.name}</span>
            </div>
          ))}
        </div>
      </aside>
      <main className="flex-1 p-8">
        <header className="mb-8">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input placeholder="Search files" className="pl-10 bg-white border-gray-200" />
          </div>
        </header>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {files.map((file) => (
            <div key={file.id} className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                {file.type === "file" && <FileIcon className="h-8 w-8 text-blue-500" />}
                {file.type === "folder" && <FolderIcon className="h-8 w-8 text-yellow-500" />}
                {file.type === "image" && <ImageIcon className="h-8 w-8 text-green-500" />}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                      <MoreVertical className="h-4 w-4" />
                      <span className="sr-only">Open menu</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Rename</DropdownMenuItem>
                    <DropdownMenuItem>Move</DropdownMenuItem>
                    <DropdownMenuItem>Delete</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
              <h3 className="font-medium text-gray-800">{file.name}</h3>
              <p className="text-sm text-gray-500 mt-1">
                {file.size} • Modified {file.modified}
              </p>
            </div>
          ))}
        </div>
      </main>
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New File</DialogTitle>
          </DialogHeader>
          <Input
            placeholder="Enter file name"
            value={newFileName}
            onChange={(e) => setNewFileName(e.target.value)}
          />
          <Button onClick={addNewFile}>Create</Button>
        </DialogContent>
      </Dialog>
    </div>
  )
}