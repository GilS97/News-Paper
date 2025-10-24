import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { useToast } from '@/components/ui/use-toast';
import { ArrowLeft, Mail, User, Sparkles } from 'lucide-react';

export default function Settings() {
  const [profile, setProfile] = useState({
    first_name: '',
    last_name: '',
    email: '',
    username: '',
    bio: '',
  });
  const [interests, setInterests] = useState([]);
  const [availableInterests, setAvailableInterests] = useState([]);
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [emailSubscription, setEmailSubscription] = useState({
    frequency: 'weekly_1',
    is_active: true,
  });
  const [loading, setLoading] = useState(true);
  const { user, updateProfile } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch profile
      const profileRes = await api.get('/users/profile/');
      setProfile(profileRes.data);

      // Fetch all interests
      const interestsRes = await api.get('/users/interests/');
      setAvailableInterests(interestsRes.data);

      // Fetch user interests
      const userInterestsRes = await api.get('/users/my-interests/');
      setSelectedInterests(userInterestsRes.data.map(ui => ui.interest.id));

      // Fetch email subscription
      const subscriptionRes = await api.get('/subscriptions/');
      setEmailSubscription(subscriptionRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    const result = await updateProfile(profile);

    if (result.success) {
      toast({
        title: 'Profil mis à jour',
        description: 'Vos informations ont été mises à jour avec succès',
      });
    } else {
      toast({
        title: 'Erreur',
        description: 'Impossible de mettre à jour le profil',
        variant: 'destructive',
      });
    }
  };

  const handleInterestToggle = async (interestId) => {
    const isSelected = selectedInterests.includes(interestId);

    try {
      if (isSelected) {
        // Find the user interest ID and remove it
        const userInterestsRes = await api.get('/users/my-interests/');
        const userInterest = userInterestsRes.data.find(
          ui => ui.interest.id === interestId
        );
        if (userInterest) {
          await api.delete(`/users/my-interests/${userInterest.id}/`);
        }
        setSelectedInterests(selectedInterests.filter(id => id !== interestId));
      } else {
        // Add interest
        await api.post('/users/my-interests/add/', {
          interest_id: interestId,
          priority: 1,
        });
        setSelectedInterests([...selectedInterests, interestId]);
      }

      toast({
        title: 'Centre d\'intérêt mis à jour',
        description: isSelected ? 'Centre d\'intérêt retiré' : 'Centre d\'intérêt ajouté',
      });
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de mettre à jour les centres d\'intérêt',
        variant: 'destructive',
      });
    }
  };

  const handleSubscriptionUpdate = async (e) => {
    e.preventDefault();

    try {
      await api.patch('/subscriptions/', emailSubscription);
      toast({
        title: 'Préférences mises à jour',
        description: 'Vos préférences d\'email ont été mises à jour',
      });
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de mettre à jour les préférences',
        variant: 'destructive',
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Chargement...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <Button
            variant="ghost"
            onClick={() => navigate('/dashboard')}
            className="gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Retour au tableau de bord
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold mb-8">Paramètres</h1>

        {/* Profile Settings */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <User className="h-5 w-5 text-primary" />
              <CardTitle>Profil</CardTitle>
            </div>
            <CardDescription>Gérez vos informations personnelles</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleProfileUpdate} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="first_name">Prénom</Label>
                  <Input
                    id="first_name"
                    value={profile.first_name}
                    onChange={(e) =>
                      setProfile({ ...profile, first_name: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="last_name">Nom</Label>
                  <Input
                    id="last_name"
                    value={profile.last_name}
                    onChange={(e) =>
                      setProfile({ ...profile, last_name: e.target.value })
                    }
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="username">Nom d'utilisateur</Label>
                <Input
                  id="username"
                  value={profile.username}
                  onChange={(e) =>
                    setProfile({ ...profile, username: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={profile.email}
                  onChange={(e) =>
                    setProfile({ ...profile, email: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <Input
                  id="bio"
                  value={profile.bio}
                  onChange={(e) =>
                    setProfile({ ...profile, bio: e.target.value })
                  }
                  placeholder="Parlez-nous de vous..."
                />
              </div>
              <Button type="submit">Mettre à jour le profil</Button>
            </form>
          </CardContent>
        </Card>

        {/* Interests Settings */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <CardTitle>Centres d'intérêt</CardTitle>
            </div>
            <CardDescription>
              Sélectionnez vos centres d'intérêt pour recevoir des articles personnalisés
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {availableInterests.map((interest) => (
                <div key={interest.id} className="flex items-center space-x-2">
                  <Checkbox
                    id={`interest-${interest.id}`}
                    checked={selectedInterests.includes(interest.id)}
                    onCheckedChange={() => handleInterestToggle(interest.id)}
                  />
                  <label
                    htmlFor={`interest-${interest.id}`}
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    {interest.name}
                  </label>
                </div>
              ))}
            </div>
            {availableInterests.length === 0 && (
              <p className="text-sm text-muted-foreground">
                Aucun centre d'intérêt disponible pour le moment
              </p>
            )}
          </CardContent>
        </Card>

        {/* Email Subscription Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Mail className="h-5 w-5 text-primary" />
              <CardTitle>Notifications par email</CardTitle>
            </div>
            <CardDescription>
              Configurez la fréquence de réception de vos digests d'articles
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubscriptionUpdate} className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="is_active"
                  checked={emailSubscription.is_active}
                  onCheckedChange={(checked) =>
                    setEmailSubscription({ ...emailSubscription, is_active: checked })
                  }
                />
                <label
                  htmlFor="is_active"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Recevoir des emails
                </label>
              </div>
              <div className="space-y-2">
                <Label htmlFor="frequency">Fréquence</Label>
                <Select
                  value={emailSubscription.frequency}
                  onValueChange={(value) =>
                    setEmailSubscription({ ...emailSubscription, frequency: value })
                  }
                  disabled={!emailSubscription.is_active}
                >
                  <SelectTrigger id="frequency">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">Aucun</SelectItem>
                    <SelectItem value="daily">Tous les jours</SelectItem>
                    <SelectItem value="weekly_1">Une fois par semaine</SelectItem>
                    <SelectItem value="weekly_2">Deux fois par semaine</SelectItem>
                    <SelectItem value="weekly_3">Trois fois par semaine</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button type="submit">Mettre à jour les préférences</Button>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
