import { useState, useEffect } from 'react'
import type { Card as CardType } from './services/api'
import { cardService } from './services/cardService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Button } from './components/ui/button'
import { Input } from './components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './components/ui/table'
import { Badge } from './components/ui/badge'

function App() {
  const [cards, setCards] = useState<CardType[]>([])
  const [filteredCards, setFilteredCards] = useState<CardType[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Add card form state
  const [newCardName, setNewCardName] = useState('')
  const [isAdding, setIsAdding] = useState(false)
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('')
  
  // Stats state
  const [stats, setStats] = useState({ total_cards: 0, total_quantity: 0, favorite_count: 0 })
  
  // Filter state
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false)

  // Load cards on mount
  useEffect(() => {
    loadCards()
  }, [])

  // Filter cards when search query or filter changes
  useEffect(() => {
    filterCards()
  }, [cards, searchQuery, showFavoritesOnly])

  const loadCards = async () => {
    try {
      setLoading(true)
      setError(null)
      const [cardsData, statsData] = await Promise.all([
        cardService.getAllCards(),
        cardService.getStats()
      ])
      setCards(cardsData)
      setStats(statsData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load cards')
      console.error('Error loading cards:', err)
    } finally {
      setLoading(false)
    }
  }

  const filterCards = () => {
    let result = [...cards]
    
    // Filter by favorites if enabled
    if (showFavoritesOnly) {
      result = result.filter(card => card.is_favorite)
    }
    
    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      result = result.filter(card => 
        card.name.toLowerCase().includes(query) ||
        card.set_name.toLowerCase().includes(query) ||
        (card.card_number && card.card_number.toLowerCase().includes(query)) ||
        (card.rarity && card.rarity.toLowerCase().includes(query))
      )
    }
    
    setFilteredCards(result)
  }

  const handleAddCard = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newCardName.trim()) return

    try {
      setIsAdding(true)
      setError(null)
      await cardService.addCard(newCardName.trim())
      setNewCardName('')
      await loadCards()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add card')
      console.error('Error adding card:', err)
    } finally {
      setIsAdding(false)
    }
  }

  const handleToggleFavorite = async (card: CardType) => {
    try {
      setError(null)
      await cardService.toggleFavorite(card.id, card.is_favorite)
      await loadCards()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update favorite')
      console.error('Error toggling favorite:', err)
    }
  }

  const handleDeleteCard = async (id: number) => {
    if (!confirm('Are you sure you want to delete this card?')) return

    try {
      setError(null)
      await cardService.deleteCard(id)
      await loadCards()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete card')
      console.error('Error deleting card:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <div className="container mx-auto p-4 max-w-7xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Pokemon Card Collection
          </h1>
          <p className="text-slate-600">
            Manage and track your Pokemon trading card collection
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            <p className="font-medium">Error: {error}</p>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">Total Cards</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">{stats.total_cards}</div>
              <p className="text-xs text-slate-500 mt-1">Unique cards in collection</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">Total Quantity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">{stats.total_quantity}</div>
              <p className="text-xs text-slate-500 mt-1">Including duplicates</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">Favorites</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">{stats.favorite_count}</div>
              <p className="text-xs text-slate-500 mt-1">Marked as favorite</p>
            </CardContent>
          </Card>
        </div>

        {/* Add Card Form */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Add New Card</CardTitle>
            <CardDescription>
              Enter the card name to add it to your collection
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddCard} className="flex gap-2">
              <Input
                type="text"
                placeholder="Card name (e.g., Charizard)"
                value={newCardName}
                onChange={(e) => setNewCardName(e.target.value)}
                disabled={isAdding}
                className="flex-1"
              />
              <Button type="submit" disabled={isAdding || !newCardName.trim()}>
                {isAdding ? 'Adding...' : 'Add Card'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Search and Filters */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <Input
                  type="text"
                  placeholder="Search cards..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <Button
                variant={showFavoritesOnly ? "default" : "outline"}
                onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
              >
                {showFavoritesOnly ? 'Show All' : 'Show Favorites'}
              </Button>
              <Button variant="outline" onClick={loadCards}>
                Refresh
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Cards Table */}
        <Card>
          <CardHeader>
            <CardTitle>
              Your Collection ({filteredCards.length} {filteredCards.length === 1 ? 'card' : 'cards'})
            </CardTitle>
            <CardDescription>
              {showFavoritesOnly ? 'Showing favorite cards only' : 'All cards in your collection'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8 text-slate-500">Loading cards...</div>
            ) : filteredCards.length === 0 ? (
              <div className="text-center py-8 text-slate-500">
                {cards.length === 0 
                  ? 'No cards in your collection yet. Add your first card above!'
                  : 'No cards match your search or filter.'
                }
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Set</TableHead>
                      <TableHead className="text-center">Number</TableHead>
                      <TableHead className="text-center">Rarity</TableHead>
                      <TableHead className="text-center">Quantity</TableHead>
                      <TableHead className="text-center">Favorite</TableHead>
                      <TableHead className="text-center">Added</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredCards.map((card) => (
                      <TableRow key={card.id}>
                        <TableCell className="font-medium">{card.name}</TableCell>
                        <TableCell>{card.set_name}</TableCell>
                        <TableCell className="text-center">
                          {card.card_number || '-'}
                        </TableCell>
                        <TableCell className="text-center">
                          {card.rarity ? (
                            <Badge variant="secondary">{card.rarity}</Badge>
                          ) : (
                            '-'
                          )}
                        </TableCell>
                        <TableCell className="text-center">
                          <Badge variant="outline">{card.quantity}</Badge>
                        </TableCell>
                        <TableCell className="text-center">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleToggleFavorite(card)}
                          >
                            {card.is_favorite ? '⭐' : '☆'}
                          </Button>
                        </TableCell>
                        <TableCell className="text-center text-sm text-slate-500">
                          {new Date(card.date_added).toLocaleDateString()}
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteCard(card.id)}
                          >
                            Delete
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-slate-500">
          <p>Trading Card Collection Manager - Built with React + FastAPI</p>
        </div>
      </div>
      </div>
  )
}

export default App
