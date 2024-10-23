'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Search, Upload, Hash, BarChart, HelpCircle, ChevronDown, ChevronUp, PieChart, LineChart } from 'lucide-react'


export default function Home() {
  const [activeSearch, setActiveSearch] = useState<'simple' | 'csv' | 'regex' | null>(null)
  const [showMoreCriteria, setShowMoreCriteria] = useState(false)
  const [searchResults, setSearchResults] = useState<{ nom: string; prenom: string; email: string; dateNaissance?: string; pieceIdentite?: string }[]>([])
  const [analysisType, setAnalysisType] = useState<'columns' | 'emails' | 'operators' | null>(null)

  const handleSimpleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setSearchResults([
      { nom: 'Doe', prenom: 'John', email: 'john@example.com', dateNaissance: '1990-01-01', pieceIdentite: 'AB123456' },
      { nom: 'Smith', prenom: 'Jane', email: 'jane@example.com', dateNaissance: '1985-05-15', pieceIdentite: 'CD789012' },
    ])
  }

  const handleCsvUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('CSV File uploaded:', e.target.files?.[0]?.name)
  }

  const handleRegexSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setSearchResults([
      { nom: 'Doe', prenom: 'John', email: 'john@example.com' },
      { nom: 'Smith', prenom: 'Jane', email: 'jane@example.com' },
    ])
  }

  const handleAnalysis = (type: 'columns' | 'emails' | 'operators') => {
    setAnalysisType(type)
    // Implement actual analysis logic here
    console.log(`Performing ${type} analysis`)
  }

  return (
    <TooltipProvider>
      <div className="container mx-auto my-auto p-4 space-y-8 max-w-4xl">
        <h1 className="text-3xl font-bold mb-6 text-center">Exploration</h1>

        <Tabs defaultValue="search" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="search">Recherche</TabsTrigger>
            <TabsTrigger value="analysis">Analyse</TabsTrigger>
          </TabsList>
          <TabsContent value="search" className="mt-6">
            <div className="grid grid-cols-3 gap-4 mb-8 max-w-md mx-auto">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      onClick={() => setActiveSearch('simple')}
                      variant={activeSearch === 'simple' ? 'default' : 'outline'}
                      className="h-24 w-24 flex-col"
                    >
                      <Search className="h-8 w-8 mb-2" />
                      Simple
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Recherche par critères simples</p>
                  </TooltipContent>
                </Tooltip>
              </motion.div>

              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      onClick={() => setActiveSearch('csv')}
                      variant={activeSearch === 'csv' ? 'default' : 'outline'}
                      className="h-24 w-24 flex-col"
                    >
                      <Upload className="h-8 w-8 mb-2" />
                      CSV
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Charger un fichier CSV</p>
                  </TooltipContent>
                </Tooltip>
              </motion.div>

              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      onClick={() => setActiveSearch('regex')}
                      variant={activeSearch === 'regex' ? 'default' : 'outline'}
                      className="h-24 w-24 flex-col"
                    >
                      <Hash className="h-8 w-8 mb-2" />
                      Regex
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Recherche par expression régulière</p>
                  </TooltipContent>
                </Tooltip>
              </motion.div>
            </div>

            {activeSearch === 'simple' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-4"
              >
                <form onSubmit={handleSimpleSearch} className="space-y-4 max-w-2xl mx-auto">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="nom">Nom</Label>
                      <Input id="nom" placeholder="Ex: Dupont" />
                    </div>
                    <div>
                      <Label htmlFor="prenom">Prénom</Label>
                      <Input id="prenom" placeholder="Ex: Marie" />
                    </div>
                  </div>
                  <AnimatePresence>
                    {showMoreCriteria && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="grid grid-cols-2 gap-4"
                      >
                        <div>
                          <Label htmlFor="email">Email</Label>
                          <Input id="email" type="email" placeholder="Ex: marie.dupont@email.com" />
                        </div>
                        <div>
                          <Label htmlFor="dateNaissance">Date de naissance</Label>
                          <Input id="dateNaissance" type="date" />
                        </div>
                        <div>
                          <Label htmlFor="pieceIdentite">Numéro de pièce d&apos;identité</Label>
                          <Input id="pieceIdentite" placeholder="Ex: 123AB4567" />
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                  <div className="flex flex-col sm:flex-row gap-4">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setShowMoreCriteria(!showMoreCriteria)}
                      className="flex-1"
                    >
                      {showMoreCriteria ? (
                        <>
                          <ChevronUp className="mr-2 h-4 w-4" /> Moins de critères
                        </>
                      ) : (
                        <>
                          <ChevronDown className="mr-2 h-4 w-4" /> Plus de critères
                        </>
                      )}
                    </Button>
                    <Button type="submit" className="flex-1">
                      <Search className="mr-2 h-4 w-4" /> Lancer la recherche
                    </Button>
                  </div>
                </form>
              </motion.div>
            )}

            {activeSearch === 'csv' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-4"
              >
                <Label htmlFor="csvFile" className="block text-center">
                  Glissez-déposez votre fichier CSV ici ou cliquez pour sélectionner
                </Label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                  <Input
                    id="csvFile"
                    type="file"
                    accept=".csv"
                    onChange={handleCsvUpload}
                    className="hidden"
                  />
                  <Label htmlFor="csvFile" className="cursor-pointer">
                    <Upload className="mx-auto h-12 w-12 text-gray-400" />
                    <span className="mt-2 block text-sm font-semibold">Sélectionner un fichier CSV</span>
                  </Label>
                </div>
              </motion.div>
            )}

            {activeSearch === 'regex' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-4"
              >
                <form onSubmit={handleRegexSearch} className="space-y-4">
                  <div>
                    <Label htmlFor="regex">Expression régulière pour les emails</Label>
                    <Input id="regex" placeholder="Ex: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" />
                  </div>
                  <Button type="submit" className="w-full">
                    <Hash className="mr-2 h-4 w-4" /> Rechercher par Regex
                  </Button>
                </form>
              </motion.div>
            )}

            {searchResults.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="mt-8 overflow-x-auto"
              >
                <Table className="w-full max-w-2xl mx-auto">
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nom</TableHead>
                      <TableHead>Prénom</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Date de naissance</TableHead>
                      <TableHead>Numéro de pièce d&apos;identité</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {searchResults.map((result, index) => (
                      <TableRow key={index}>
                        <TableCell>{result.nom}</TableCell>
                        <TableCell>{result.prenom}</TableCell>
                        <TableCell>{result.email}</TableCell>
                        <TableCell>{result.dateNaissance}</TableCell>
                        <TableCell>{result.pieceIdentite}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </motion.div>
            )}
          </TabsContent>
          <TabsContent value="analysis" className="mt-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  onClick={() => handleAnalysis('columns')}
                  variant={analysisType === 'columns' ? 'default' : 'outline'}
                  className="w-full h-24 flex-col"
                >
                  <BarChart className="h-8 w-8 mb-2" />
                  Toutes les colonnes
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  onClick={() => handleAnalysis('emails')}
                  variant={analysisType === 'emails' ? 'default' : 'outline'}
                  className="w-full h-24 flex-col"
                >
                  <PieChart className="h-8 w-8 mb-2" />
                  Emails et téléphones
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  onClick={() => handleAnalysis('operators')}
                  variant={analysisType === 'operators' ? 'default' : 'outline'}
                  className="w-full h-24 flex-col"
                >
                  <LineChart className="h-8 w-8 mb-2" />
                  Emails et opérateurs
                </Button>
              </motion.div>
            </div>
            {analysisType && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="mt-8 p-4 bg-muted rounded-lg"
              >
                <h2 className="text-lg font-semibold mb-2">Résultats de l&apos;analyse : {analysisType}</h2>
                <p>Les résultats de l&apos;analyse seront affichés ici.</p>
              </motion.div>
            )}
          </TabsContent>
        </Tabs>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon" className="absolute bottom-4 right-4">
              <HelpCircle className="h-6 w-6" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Besoin d&apos;aide ? Cliquez ici pour un guide rapide !</p>
          </TooltipContent>
        </Tooltip>
      </div>
    </TooltipProvider>
  )
}