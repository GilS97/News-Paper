import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/components/ui/use-toast';
import { Newspaper, Settings, LogOut, Heart, Bookmark, ExternalLink, Search } from 'lucide-react';
import { Input } from '@/components/ui/input';

export default function Dashboard() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      const response = await api.get('/articles/');
      setArticles(response.data.results || response.data);
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de charger les articles',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveArticle = async (articleId) => {
    try {
      await api.post(`/articles/${articleId}/save/`);
      toast({
        title: 'Article sauvegardé',
        description: 'L\'article a été ajouté à vos favoris',
      });
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de sauvegarder l\'article',
        variant: 'destructive',
      });
    }
  };

  const handleLikeArticle = async (articleId) => {
    try {
      await api.post(`/articles/${articleId}/like/`);
      toast({
        title: 'Article aimé',
        description: 'Merci pour votre feedback!',
      });
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible d\'aimer l\'article',
        variant: 'destructive',
      });
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const filteredArticles = articles.filter((article) =>
    article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    article.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Chargement des articles...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <Newspaper className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold">News Paper</h1>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground hidden sm:inline">
                Bonjour, {user?.first_name || user?.username}
              </span>
              <Button
                variant="outline"
                size="icon"
                onClick={() => navigate('/settings')}
              >
                <Settings className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="icon" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative max-w-2xl mx-auto">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Rechercher des articles..."
              className="pl-10"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* No interests message */}
        {user?.interests?.length === 0 && (
          <Card className="mb-8 border-primary">
            <CardHeader>
              <CardTitle>Configurez vos centres d'intérêt</CardTitle>
              <CardDescription>
                Pour recevoir des articles personnalisés, veuillez ajouter vos centres d'intérêt dans les paramètres.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={() => navigate('/settings')}>
                Aller aux paramètres
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Articles Grid */}
        {filteredArticles.length === 0 ? (
          <Card className="max-w-2xl mx-auto">
            <CardContent className="text-center py-12">
              <p className="text-muted-foreground">
                {searchQuery
                  ? 'Aucun article ne correspond à votre recherche'
                  : 'Aucun article disponible pour le moment'}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredArticles.map((article) => (
              <Card key={article.id} className="flex flex-col hover:shadow-lg transition-shadow">
                {article.image_url && (
                  <img
                    src={article.image_url}
                    alt={article.title}
                    className="w-full h-48 object-cover rounded-t-lg"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                )}
                <CardHeader>
                  <CardTitle className="line-clamp-2 text-lg">
                    {article.title}
                  </CardTitle>
                  <CardDescription className="line-clamp-1">
                    {article.source_name}
                    {article.author && ` • ${article.author}`}
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-grow">
                  <p className="text-sm text-muted-foreground line-clamp-3">
                    {article.description}
                  </p>
                  {article.interest_names && article.interest_names.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-3">
                      {article.interest_names.map((interest, idx) => (
                        <span
                          key={idx}
                          className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full"
                        >
                          {interest}
                        </span>
                      ))}
                    </div>
                  )}
                </CardContent>
                <CardContent className="pt-0">
                  <div className="flex items-center justify-between">
                    <div className="flex gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleLikeArticle(article.id)}
                      >
                        <Heart className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleSaveArticle(article.id)}
                      >
                        <Bookmark className="h-4 w-4" />
                      </Button>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open(article.url, '_blank')}
                    >
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Lire
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
